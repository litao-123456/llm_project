from pymilvus import MilvusClient,DataType
import os
import pandas as pd
from openai import OpenAI

from embedding.embedding转换向量数据 import embedding_model

embedding_model = "text-embedding-v4"
embedding_client = OpenAI(api_key="sk-6f65e37d8d0e4e9d9d5c81431ef50522",base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
milvus_client = MilvusClient("http://192.168.11.128:19530")

DIMENSIONS = 1024
save_len = 0
# 向量化
def get_embedding(text):
    global save_len
    response_data = embedding_client.embeddings.create(input=text,model=embedding_model,dimensions=DIMENSIONS)
    embedding = response_data.data[0].embedding
    if len(embedding) == DIMENSIONS:
        save_len += 1
        print(f"已向量化{save_len}个")
        return embedding
    return [0.0] * DIMENSIONS


# 创建向量库
def create_collection(collection_name):
    if milvus_client.has_collection(collection_name):
        print(f"{collection_name} is ready")
        return
    # 1. 创建 schema
    schema = milvus_client.create_schema(
        auto_id=True,  # 自动生成主键 ID
        enable_dynamic_fields=True  # 允许插入未定义的额外字段（可选，方便调试）
    )

    # 2. 添加字段
    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="Time", datatype=DataType.INT64)
    schema.add_field(field_name="UserId", datatype=DataType.VARCHAR, max_length=64)
    schema.add_field(field_name="Score", datatype=DataType.FLOAT)
    schema.add_field(field_name="combined", datatype=DataType.VARCHAR, max_length=65535)
    schema.add_field(field_name="embedding_data", datatype=DataType.FLOAT_VECTOR, dim=DIMENSIONS)

    # 3. 准备索引参数（向量字段必须建索引才能高效搜索）
    index_params = milvus_client.prepare_index_params()
    index_params.add_index(
        field_name="embedding_data",
        index_type="IVF_FLAT",  # 简单准确，适合小数据集（< 10万条）
        metric_type="COSINE",  # 余弦相似度（和 DashScope Embedding 匹配）
        params={"nlist": 128}  # IVF 分成 128 个聚类单元
    )

    # 4. 创建集合
    milvus_client.create_collection(
        collection_name=collection_name,
        schema=schema,
        index_params=index_params
    )

    print(f"🎉 Collection '{collection_name}' created successfully with vector index!")


# 保存数据到向量库中
def save_embedding(df_batch: pd.DataFrame,collection_name):
    data_to_insert = []
    for index, row in df_batch.iterrows():
        record = {
            "Time": int(row["Time"]) if pd.notna(row["Time"]) else 0,
            "UserId": str(row["UserId"]) if pd.notna(row["UserId"]) else "",
            "Score": float(row["Score"]) if pd.notna(row["Score"]) else 0.0,
            "combined": str(row["combined"]) if pd.notna(row["combined"]) else "",
            "embedding_data": row["embedding_data"]
        }
        data_to_insert.append(record)
    milvus_client.insert(collection_name=collection_name,data=data_to_insert)
    print(f"Inserted {len(data_to_insert)} records into Milvus.")



if __name__ == '__main__':
    # 读取 scv文件
    df = pd.read_csv("data/fine_food_reviews_1k.csv")
    df['combined'] = "Title:" + df.Summary.str.strip() + "; Content:" + df.Text.str.strip()
    # 向量化数据
    df['embedding_data'] = df['combined'].apply(get_embedding)

    create_collection(collection_name="YMX")

    save_embedding(df,collection_name="YMX")

    print("All data inserted into Milvus!")
