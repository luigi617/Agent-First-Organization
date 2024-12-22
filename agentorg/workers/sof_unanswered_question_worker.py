import logging
import requests  # Import requests library for HTTP requests

from langgraph.graph import StateGraph, START
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate

from agentorg.workers.worker import BaseWorker, register_worker
from agentorg.workers.prompts import tags_extraction_prompt
from agentorg.utils.graph_state import MessageState
from agentorg.utils.model_config import MODEL
from agentorg.utils.utils import chunk_string, postprocess_json



logger = logging.getLogger(__name__)

@register_worker
class SOFUnansweredQuestionWorker(BaseWorker):

    description = "Give a list of Stack Overflow unanswered questions given a list of tags extracted from historical conversation"

    def __init__(self):
        super().__init__()
        self.action_graph = self._create_action_graph()
        self.llm = ChatOpenAI(model=MODEL["model_type_or_path"], timeout=30000)
        self.api_url = "https://api.stackexchange.com/2.3/questions/no-answers"

    def _create_action_graph(self):
        workflow = StateGraph(MessageState)
        workflow.add_node("generator", self.generator)
        workflow.add_edge(START, "generator")
        return workflow

    def generator(self, state: MessageState):

        historical_conversation = state["user_message"].history
        prompt = PromptTemplate.from_template(tags_extraction_prompt)
        input_prompt = prompt.invoke({"conversation": historical_conversation})
        logger.info(f"Prompt: {input_prompt.text}")
        chunked_prompt = chunk_string(input_prompt.text, tokenizer=MODEL["tokenizer"], max_length=MODEL["context"])
        final_chain = self.llm | StrOutputParser()
        answer = final_chain.invoke(chunked_prompt)
        answer = postprocess_json(answer)
        
        params = {
            "order": "desc",
            "sort": "activity",
            "tagged": answer["message"],
            "site": "stackoverflow"
        }

        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            items = data.get("items", [])
            result = []
            for item in items:
                title = item.get("title", "No title")
                link = item.get("link", "No link")
                tags = ", ".join(item.get("tags", []))
                result.append(f"Title: {title}\nLink: {link}\nTags: {tags}\n")
            output = "\n".join(result)

            state["message_flow"] = ""
            state["response"] = output
            return state

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from Stack Exchange API: {e}")
            state["message_flow"] = ""
            state["response"] = "Error fetching data from Stack Exchange API."
            return state


    def execute(self, msg_state: MessageState):
        graph = self.action_graph.compile()
        result = graph.invoke(msg_state)
        return result