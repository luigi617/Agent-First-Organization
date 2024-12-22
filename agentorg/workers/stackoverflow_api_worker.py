import logging
import requests  # Import requests library for HTTP requests

from langgraph.graph import StateGraph, START
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate

from agentorg.workers.tools.StackOverflow import StackOverflow
from agentorg.workers.worker import BaseWorker, register_worker
from agentorg.workers.prompts import api_selection_function_call_prompt, elaborate_output_from_api_call_prompt
from agentorg.utils.graph_state import MessageState
from agentorg.utils.model_config import MODEL
from agentorg.utils.utils import chunk_string, postprocess_json
import os
import json


logger = logging.getLogger(__name__)


@register_worker
class StackOverflowAPIWorker(BaseWorker):

    description = "The StackOverflow worker, which calls StackOverflow APIs to retrieve lists of tags, answers, comments, or questions sorted by activity, creation, or votes; retrieve answers, comments, or questions by their IDs; fetch answers or comments by question ID; and retrieve related, unanswered, or minimally answered questions; the worker is not useful when the agent needs to ask the user for clarification about tags or topics."

    def __init__(self):
        super().__init__()
        self.action_graph = self._create_action_graph()
        self.llm = ChatOpenAI(model=MODEL["model_type_or_path"], timeout=30000)

    def _create_action_graph(self):
        workflow = StateGraph(MessageState)
        workflow.add_node("generator", self.generator)
        workflow.add_edge(START, "generator")
        return workflow

    def generator(self, state: MessageState):
        historical_conversation = state["user_message"].history
        import json
        filepath = os.path.join("./examples/stackoverflow_assistant", "api_information.json")
        with open(filepath) as f:
            api_all_info = json.load(f)
        input_prompt = api_selection_function_call_prompt + "User task:" + historical_conversation + "List of APIs information:" + str(api_all_info) + "Answer:"
        chunked_prompt = chunk_string(input_prompt, tokenizer=MODEL["tokenizer"], max_length=MODEL["context"])
        final_chain = self.llm | StrOutputParser()
        answer = final_chain.invoke(chunked_prompt)
        answer_propessed = False
        try:
            answer = postprocess_json(answer)
            answer_propessed = True
        except:
            api_called = "No API is called"
            api_call_output = answer

        if answer_propessed:
            try:
                api_called, api_call_output = StackOverflow.api_call(answer["api"], answer["parameters"])
            except Exception as e:
                logger.error(f"Error fetching data from Stack Exchange API: {e}")
                state["message_flow"] = ""
                state["response"] = "Error fetching data from Stack Exchange API."
                return state



        prompt = PromptTemplate.from_template(elaborate_output_from_api_call_prompt)
        input_prompt = prompt.invoke({"user_task": historical_conversation, "api_url": api_called, "api_output": api_call_output})
        chunked_prompt = chunk_string(input_prompt.text, tokenizer=MODEL["tokenizer"], max_length=MODEL["context"])
        final_chain = self.llm | StrOutputParser()
        answer = final_chain.invoke(chunked_prompt)
        answer = postprocess_json(answer)

        state["message_flow"] = ""
        state["response"] = answer.get("message", "Error in elaborating the output.")

        return state


    def execute(self, msg_state: MessageState):
        graph = self.action_graph.compile()
        result = graph.invoke(msg_state)
        return result