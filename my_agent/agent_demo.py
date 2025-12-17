import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from my_agent import query_api
import yaml


class AgentDemo:

    @classmethod
    def get_langchain_llm(self):
        api_key = "sk-c5b37ad58afd4d1aa1a0924a93a7459f"
        llm = ChatOpenAI(
            model="qwen-plus",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=api_key,
            temperature=0.7,
            streaming=True,
        )
        return llm

    @classmethod
    def get_prompt(self, template_name):
        with open("D:\python_code\my_code\FastAPIProject\env\prompt.yml", 'r', encoding='utf-8') as f:
            prompts = yaml.safe_load(f)
        return prompts.get(template_name)

    @classmethod
    def get_llm(cls, query):
        query_type = cls.get_prompt(template_name="query_type")
        prompt = PromptTemplate(
            input_variables=["query"],
            template=query_type,
        )
        llm = cls.get_langchain_llm()
        formatted_prompt = prompt.format(query=query)
        type_llm = llm.invoke(formatted_prompt)
        result = json.loads(type_llm.content)
        print(result)
        data_type = result.get("type")
        llm_data = result.get("data")
        print(llm_data)
        res = {}
        # 根据type 获取对应的 tool
        if "car" in data_type:
            res = query_api.query_car_code(llm_data)
        elif "flower" in data_type:
            res = query_api.query_flower(llm_data)
        elif "animal" in data_type:
            res = query_api.query_dog_api(llm_data)
        # 根据type 获取不同的prompt
        detail_prompt = cls.get_prompt(template_name=data_type)
        format_prompt = detail_prompt.format(query=res.get("query"), detail=res.get("detail"))
        print(format_prompt)
        detail_llm = llm.stream(format_prompt)
        all_str = ""
        for chunk in detail_llm:
            print(f"data:{chunk.content}")
            all_str += chunk.content
        print(f"完整的输出为：{all_str}")


if __name__ == '__main__':
    agent = AgentDemo()
    query = "加菲猫怎么样？"
    agent.get_llm(query)

"""
第一步，初始化prompt,读取prompt的文件
第二步，初始化Tool,调用不同的API
第三步，意图识别--> 根据返回值调用不同的API，丰富对应的prompt 输出
"""
