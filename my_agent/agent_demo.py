from langchain.agents import *
from langchain_classic.chains.summarize.refine_prompts import prompt_template
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI  # 推荐新写法
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
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
    def get_prompt(self,template_name):
        with open("D:\python_code\my_code\FastAPIProject\env\prompt.yml",'r',encoding='utf-8') as f:
            prompts = yaml.safe_load(f)
        return prompts.get(template_name)

    @classmethod
    def get_llm(cls, query):
        query_type = cls.get_prompt(template_name="query_type")
        print(query_type)
        prompt = PromptTemplate(
            input_variables=["query"],
            template=query_type,
        )
        llm = cls.get_langchain_llm()
        formatted_prompt = prompt.format(query=query)
        type_llm = llm.invoke(formatted_prompt)
        print(type_llm.content)

if __name__ == '__main__':
    agent = AgentDemo()
    query = "帮我看下这个车牌号是什么情况，京A98754"
    agent.get_llm(query)



"""
第一步，初始化prompt,读取prompt的文件
第二步，初始化Tool,调用不同的API
第三步，意图识别--> 根据返回值调用不同的API，丰富对应的prompt 输出
"""
