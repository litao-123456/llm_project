import json
import sys

import yaml
from langchain_core.runnables import RunnableSequence
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI  # 关键！阿里云百炼适配器
from sqlalchemy import false


class SimpleChainServices:

    # 获取连接
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

    # 读取 yaml
    @classmethod
    def get_prompt_template(self):
        file_path = "D:\python_code\my_code\FastAPIProject\env\prompt.yml"
        with open(file_path,'r',encoding='utf-8') as f:
            prompts = yaml.load(f, Loader=yaml.FullLoader)
            return prompts.get("query_car_prompt")

    # 创建问答链 注意问答时，组装，再询问，顺序不能放反
    @classmethod
    def create_simple_chains(self,query):
        print("query:", query)
        llm = self.get_langchain_llm()
        prompt_template = self.get_prompt_template()
        prompt = PromptTemplate(
            input_variables=["query"],
            template=prompt_template,
        )

        #创建链
        chains = prompt | llm

        print("-----begin---------")
        print(f"prompt: {prompt_template.format(query=query)}")
        response_stream = chains.stream({"query": query})
        for chunk in response_stream:
            payload = {"event": "test_event", "message": chunk.content}
            yield f"data: {json.dumps(payload,ensure_ascii=False)}\n\n".encode("utf-8")

    # 记忆
    def create_memory_chains(self,query:str):
        llm = self.get_langchain_llm()





if __name__ == '__main__':
    simple = SimpleChainServices()
    simple.create_simple_chains("10万的轿车有什么推荐？")



