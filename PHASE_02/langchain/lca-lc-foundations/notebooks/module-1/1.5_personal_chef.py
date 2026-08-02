from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.tools import tool
from tavily import TavilyClient

from langgraph.checkpoint.memory import InMemorySaver

import base64
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

model = init_chat_model(model="gpt-5-nano")

@tool
def web_search(query: str):

    """
    Search for the query on the internet
    """

    tavily_client = TavilyClient()

    search = tavily_client.search(query)

    return search

system_prompt = """
You are an expert chef who helps people find recipes on the internet.

If there's an image, analyze the image then give response accrdingly.

Use your tools to search the internet for the recipes. 

Use the web_search tool then give response. Give very precise response. Short responses.
"""

chef_agent = create_agent(
    model=model,
    tools=[web_search],
    system_prompt=system_prompt,
    checkpointer=InMemorySaver())

image_path = Path("fridge-5452069.webp")

img_b64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")

question = HumanMessage(content=[
    {"type":"text", "text":"these are some leftovers in the refrigerator. what recipe should I make? give 2 recipes."},
    {"type": "image", "base64": img_b64, "mime_type": "image/png"}
])

config = {"configurable":{"thread_id":2}}

result = chef_agent.invoke(
    {
        "messages":[question]
    },
    config=config,
)

print("==> AI RESPONSE: ", result["messages"][-1].content)