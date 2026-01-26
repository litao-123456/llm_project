from langchain.agents import create_agent
from car_agent.llm_tools import llm_tools
from langchain_core.prompts import PromptTemplate


def check_agent(query: str, data_type: str):
    res = {}
    # 根据type 获取对应的 tool
    if "car" in data_type:
        res = llm_tools.query_car_code(query)
    elif "flower" in data_type:
        res = llm_tools.query_flower(query)
    elif "animal" in data_type:
        res = llm_tools.query_dog_api(query)
    if res is not None:
        return llm_tools.format_response(res)
    return None


