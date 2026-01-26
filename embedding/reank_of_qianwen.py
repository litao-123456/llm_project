import os
import requests
from openai import OpenAI
from pymilvus import MilvusClient

# === 配置 ===
DASHSCOPE_API_KEY = "sk-6f65e37d8d0e4e9d9d5c81431ef50522"
EMBEDDING_MODEL = "text-embedding-v4"
RERANK_MODEL = "qwen3-rerank"

# OpenAI 兼容客户端（仅用于 embedding）
openai_client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/v1",  # 修正 URL
)

milvus_client = MilvusClient("http://192.168.11.128:19530")
COLLECTION_NAME = "YMX"


# === 1. 文本向量化 ===
def embedding_text(text: str) -> list[float]:
    response = openai_client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL,
        dimensions=1024  # text-embedding-v4 支持动态维度
    )
    return response.data[0].embedding


# === 2. Milvus 向量检索（修正为 search）===
def query_milvus(query_vector: list[float], top_k: int = 10):
    """
    使用向量在 Milvus 中进行 ANN 搜索
    假设 collection 中有字段: id, text, embedding
    """
    search_params = {
        "metric_type": "COSINE",  # 或 IP / L2，根据你的索引设置
        "params": {"nprobe": 10}
    }
    results = milvus_client.search(
        collection_name=COLLECTION_NAME,
        data=[query_vector],  # 注意：传入列表 of vectors
        limit=top_k,
        output_fields=["embedding_data"],  # 假设你存储了原始文本在 "text" 字段
        search_params=search_params
    )
    # 提取 hits
    hits = results[0]  # 因为只搜一个 query
    documents = []
    for hit in hits:
        doc = {
            "id": hit["id"],
            "text": hit["combined"]["text"],
            "score": hit["distance"]  # 注意：COSINE 越大越相似，但 Milvus 返回的是 distance（1 - cosine）
        }
        documents.append(doc)
    return documents


# === 3. 调用 DashScope 原生 rerank API ===
def rerank_with_dashscope(query: str, documents: list[dict]) -> list[dict]:
    """
    使用 DashScope qwen3-rerank 对候选文档重排序
    """
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-ranking/rerank"
    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json"
    }
    # 提取纯文本列表
    texts = [doc["text"] for doc in documents]

    payload = {
        "model": RERANK_MODEL,
        "query": query,
        "documents": texts,
        "top_n": len(texts)  # 返回全部，由你决定是否截断
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Rerank API error: {response.status_code}, {response.text}")
        return documents  # fallback

    result = response.json()
    reranked = []
    for item in result["output"]["results"]:
        idx = item["index"]
        reranked.append({
            "id": documents[idx]["id"],
            "text": documents[idx]["text"],
            "rerank_score": item["relevance_score"]
        })
    # 按 rerank_score 降序（API 已排序，但保险起见）
    reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
    return reranked


# === 4. 主流程 ===
def query_rerank(query: str, top_k: int = 10):
    # Step 1: Embedding
    query_emb = embedding_text(query)
    print(f"[INFO] Query embedded (dim={len(query_emb)})")

    # Step 2: Milvus ANN search
    milvus_results = query_milvus(query_emb, top_k=top_k)
    print(f"[INFO] Retrieved {len(milvus_results)} candidates from Milvus")

    if not milvus_results:
        return []

    # Step 3: Rerank
    reranked_results = rerank_with_dashscope(query, milvus_results)
    print(f"[INFO] Reranked {len(reranked_results)} results")

    return reranked_results


# === 测试 ===
if __name__ == '__main__':
    query = "Nice"
    results = query_rerank(query, top_k=5)
    for i, res in enumerate(results[:3], 1):
        print(f"{i}. Score: {res['rerank_score']:.4f} | Text: {res['text'][:100]}...")