# 参考文献：https://blog.csdn.net/u013172930/article/details/147861272
# langchain 将大模型的组件 ，都封装进去，可以快速的开发llm API
# chain 管道式组件，可以让模型顺序执行，例如 prompt | llm | DB 线性流

# langgraph 可以执行复杂的工作流，可以定制节点，自定义工作流，增加审批等
"""
langgraph 的核心组件
    节点（Nodes） 表示具体的操作或任务（如调用 LLM、执行工具、处理输入等）。
    边（Edges） 定义了节点之间的连接和执行顺序（可以是有条件的）。
    状态（State） 是一个贯穿整个图的数据结构，用于存储和传递信息。

LangGraph 的工作原理

    定义状态：创建一个状态对象，定义工作流中需要跟踪的数据结构。
    创建节点：编写节点函数，每个函数实现一个任务（如调用 LLM 或处理数据）。
    定义边：指定节点之间的连接逻辑，包括条件跳转。
    构建图：使用 LangGraph 的 API（通常是 StateGraph）将节点和边组合成一个图。

"""


from langgraph.graph import StateGraph, MessagesState
from typing import *

# 定义状态
class State(TypedDict):
    input:str
    output:str

# 定义节点 1
def node_1(state: State) -> State:
    state['output'] = f"处理输入{state['input']}"
    return state

# 定义节点 2
def node_2(state: State) -> State:
    state['output'] += '已完成'
    return state


# 创建图
workflow = StateGraph(State)
workflow.add_node("node_1",node_1) # 创建节点
workflow.add_node("node_2",node_2)
workflow.add_edge("node_1", "node_2") # 创建连接点
workflow.set_entry_point("node_1") # 创建开始节点
workflow.set_finish_point("node_2") # 创建结束节点


# 编译和运行
graph = workflow.compile()
result = graph.invoke({"input": "Hello, LangGraph!"})

graph_png = graph.get_graph().draw_mermaid_png()
with open("test_graph.png", "wb") as f:
    f.write(graph_png)


print(result)


 # 来自官方的 demo
def plan_demo():
    from langgraph.graph import StateGraph,MessageGraph,START,END

    def mock_llm(state: MessagesState) -> State:
        return {"message":[{"role":"user","content":"hi"}]}

    graph = StateGraph(MessagesState)
    graph.add_node(mock_llm)
    graph.add_edge(START,"mock_llm")
    graph.add_edge("mock_llm",END)
    graph = graph.compile()
    result = graph.invoke({"message":[{"role":"user","content":"hello"}]})
    graph_png = graph.get_graph().draw_mermaid_png()
    with open("plan_graph.png", "wb") as f:
        f.write(graph_png)
    print(result)


if __name__ == '__main__':
    plan_demo()








