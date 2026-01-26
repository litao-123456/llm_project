from typing import Annotated

from car_agent.llm_template import init_client
import asyncio
from langgraph.graph import StateGraph,START
from langgraph.graph.message import add_messages


class State(StateGraph):
    messages: Annotated[list,add_messages]





# 意图识别
async def car_agent():
    print("car_agent")
    asyncio.create_task(run())




async def run():
    print("run")

# task

# tools

# llm









if __name__ == '__main__':
    res = init_client.car_agent_milvus.similarity_search(query="奥迪", k=3, metric="cosine")
    for index, item in enumerate(res):
        print(index,item)

