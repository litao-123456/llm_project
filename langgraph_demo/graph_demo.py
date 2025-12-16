# langgraph 聊天机器人
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph,START
from langgraph.graph.message import add_messages
from langchain_community.chat_models import ChatOpenAI

class State(TypedDict):
    messages: Annotated[list,add_messages]

graph_builder = StateGraph(State)

api_key = "sk-c5b37ad58afd4d1aa1a0924a93a7459f"

llm = ChatOpenAI(
    api_key=api_key,
    model="qwen-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    streaming=True
)

def chatbot(state: State):
    print(f"state:{state}")
    return {"messages":[llm.invoke(state["messages"])]}

# 添加节点
graph_builder.add_node("chatbot",chatbot)

# 添加入口节点
graph_builder.add_edge(START,"chatbot")

# 编译图
graph = graph_builder.compile()

def stream_graph_updates(user_input:str):
    print(f"现在用户提问的问题是：{user_input}")
    for event in graph.stream({"messages":[{"role":"user","content":user_input}]}):
        for value in event.values():
            content = value["messages"][-1].content
            print(f"Assistant:{content}")


while True:
    try:
        user_input = input("user:")
        if user_input == "exit":
            break
        stream_graph_updates(user_input)
    except Exception as e:
        print(f"is error:{e}")
        break


#