import openai
import os
from dotenv import load_dotenv
from dotenv import dotenv_values, find_dotenv
from langchain_community.tools import TavilySearchResults


# env_config = dotenv_values(".env")  # Path to your .env file
# for key, value in env_config.items():
#     if 'KEY' in key or 'SECRET' in key:
#         print(f"{key}: {value}")
# dotenv_path = find_dotenv()
# print("Found .env at:", dotenv_path)


# print("Current Working Directory:", os.getcwd())
load_dotenv(override=True)
# for key, value in os.environ.items():
#     if 'KEY' in key or 'SECRET' in key:  # Modify this based on the key's name
#         print(f"{key}: {value}")

search_tool = TavilySearchResults(
            max_results=5,
            search_depth="advanced",
            include_answer=True,
            include_raw_content=True,
            include_images=False,
        )

query = "Debug this error: TypeError: 'type' object is not subscriptable Python. Search answer in StackOverFlow, output the id of the questions and/or results"
search_results = search_tool.invoke({"query": query})
print(search_results)


