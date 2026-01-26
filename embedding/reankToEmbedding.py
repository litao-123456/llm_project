import json
import os

import requests
from openai import OpenAI
from pymilvus import MilvusClient

# 引入向量化模型
API_KEY = "sk-6f65e37d8d0e4e9d9d5c81431ef50522"
openai_client = OpenAI(
    api_key=API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
milvus_client = MilvusClient("http://192.168.11.128:19530")

embedding_model = "text-embedding-v4"
rerank_model = "qwen3-rerank"

# 构建向量化文本方法
def embedding_text(text):
    response = openai_client.embeddings.create(input=text, model=embedding_model, dimensions=1024)
    print(f"query:{text},for embedding is: {response}")
    return response.data[0].embedding


# 使用 milvus 查询向量库
def query_milieus(embedding_query, top_k):
    query_result = milvus_client.search(collection_name="YMX",  # 查询哪个表
                                        data=[embedding_query],  # 查询内容
                                        limit=top_k,  # 查询条数
                                        output_fields=["embedding_data","combined","id"],  # 要查询哪个字段
                                        search_params={
                                            "metric_name": "L2",  # 怎么查
                                            "params": {"nprobe": 10}  # 查询相关点
                                        })
    data_list = []
    print(f"{len(query_result)} results")
    for result_list in query_result:
        for result in result_list:
            print( result.get("id"),result.get("combined"))
            data_list.append({
                "id": result.get("id"),
                "text": result.get("combined"),
            })
    return data_list


# 根据rerank 精度筛选
def rerank_filter(query:str,top_k:str,documents:list) -> list[dict]:
    url = "https://dashscope.aliyuncs.com/compatible-api/v1/reranks"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    # 提取纯文本列表（是向量化后的数据？）
    print(f"在向量库里查询的数据是：{documents}")
    req_documents = [doc["text"] for doc in documents]
    payload = {
        "model": rerank_model,
        "query": query,
        "documents": req_documents,
        "top_n": top_k
    }
    print(f"payload:{json.dumps(payload,indent=4)}")
    response = requests.post(url, headers=headers, json=payload)
    print(response.json())
    """
     阿里云返回值：
     {'object': 'list', 'results': [{'index': 7, 'relevance_score': 0.6593379545799125}, {'index': 8, 'relevance_score': 0.6593379545799125}, {'index': 9, 'relevance_score': 0.6593379545799125}], 'model': 'qwen3-rerank', 'id': '408a4632-361a-997b-a4da-bea3f8574f39', 'usage': {'total_tokens': 542}}

    """

    results = response.json().get("results")
    reranked = []

    # 将传入的list，获取到对应的index，取对应的index 里的值。作为精排筛选
    for index in results:
        print(index)
        idx = index["index"]
        reranked.append({
            "id": documents[idx]["id"],
            "text": documents[idx]["text"]
        })
    return reranked

def query_rerank(query):
    em_text = embedding_text(query)
    print(f"向量化后的query是{em_text}")
    milvus_result = query_milieus(em_text, 10)
    print(f"查询向量库相似度的文本是：{len(milvus_result)}")


if __name__ == '__main__':
    query = "Nice coffee"
    # 先将query 进行向量化
    query_embedding = embedding_text(query)
    # 查询向量数据库
    milvus_result = query_milieus(query_embedding, 10)
    # 查询rerank 进行精细排序
    rerank_result = rerank_filter(query, 3, milvus_result)
    print(rerank_result)
    print(f"{len(rerank_result)} results")