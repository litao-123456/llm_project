from typing import List

from langchain_core.embeddings import Embeddings
from env.config import conf
import requests


"""
    实例化向量类时，必须新增两个方法，一个是单个 embed_query 一个是 embed_documents
    
    使用时可以穿单个，或者list,模型会自动选择

"""


class QwenEmbedding(Embeddings):
    def __init__(self):
        self.api_key = conf.embedding_api_key

    def embed_query(self, text:str) ->List[float]:
        response = requests.post(
            url="https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings",
            headers={"Authorization":f"Bearer {self.api_key}"},
            json={
                "input": text,
                "model":conf.embedding_model
            },
        )
        return response.json().get("data")[0].get("embedding")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        response = requests.post(
            url="https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings",
            headers={"Authorization":f"Bearer {self.api_key}"},
            json={
                "input": texts,
                "model":conf.embedding_model
            },
        )
        return [item["embedding"] for item in response.json()["data"]]

qwen_embedding = QwenEmbedding()

if __name__ == '__main__':
    resp = qwen_embedding.embed_documents(["你好","我好","大家好"])
    for index,item in enumerate(resp):
        print(f"目前输出：{index},内容是：{item}")