from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage, AIMessage
import uuid
import sqlite3
#tools
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

import os
import requests

from langgraph.graph.message import add_messages

load_dotenv(override=True)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


#*****************tools********************
search_tool = DuckDuckGoSearchRun(region="us-en")

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}
    
@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA') 
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=C9PE94QUEW9VWGFM"
    r = requests.get(url)
    return r.json()


tools = [search_tool, get_stock_price, calculator]
llm_with_tools = llm.bind_tools(tools)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    #take user query from state 
    messages =state['messages']


    #sent to llm
    response = llm.invoke(messages)

    #responce store state
    return {'messages': [response]}

tool_node = ToolNode(tools)
 
#checkpointers
conn =sqlite3.connect(database='chatbot.db', check_same_thread= False)
checkpointer = SqliteSaver(conn = conn)

graph =StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, 'chat_node')
graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge('tools', 'chat_node')

chatbot = graph.compile(checkpointer=checkpointer)

# CONFIG= { 'configurable ': {'thread_id': 'thread-1'}}
# response = chatbot.invoke(
#     {
#         'messages': [HumanMessage(content ='Hi my name is veenus')]
#     },
#     config = CONFIG )

# print(response)
def retrieve_all_threads():

    all_threads = {}

    seen_threads = set()

    for checkpoint in checkpointer.list(None):

        thread_id = checkpoint.config["configurable"]["thread_id"]

        if thread_id in seen_threads:
            continue

        seen_threads.add(thread_id)

        messages = checkpoint.checkpoint.get(
            "channel_values",
            {}
        ).get(
            "messages",
            []
        )

        title = "New Chat"

        for msg in messages:

            if isinstance(msg, HumanMessage):

                content = msg.content

                if isinstance(content, list):

                    final_text = ""

                    for item in content:

                        if (
                            isinstance(item, dict)
                            and item.get("type") == "text"
                        ):
                            final_text += item.get("text", "")

                    content = final_text

                title = content[:30]
                break

        all_threads[thread_id] = title

    return all_threads

