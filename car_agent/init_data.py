import json
from openai import OpenAI
from pymilvus import MilvusClient, DataType
import time

from env.config import conf

milvus_client = MilvusClient(uri=conf.milvus_client_url)

embedding_client = OpenAI(api_key=conf.embedding_api_key, base_url=conf.embedding_url)


# 构建向量化字段
def build_milvus():
    print("milvus_client is init.......")

    # 1.创建模式
    schema = milvus_client.create_schema(auto_id=True, enable_dynamic_fields=True)

    # 2.创建字段
    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="Time", datatype=DataType.FLOAT)
    schema.add_field(field_name="name", datatype=DataType.VARCHAR,max_length=64)
    schema.add_field(field_name="price", datatype=DataType.FLOAT)
    schema.add_field(field_name="description", datatype=DataType.VARCHAR,max_length=65535)
    schema.add_field(field_name="vector_data", datatype=DataType.FLOAT_VECTOR, dim=1024)

    # 3.准备索引参数
    index_params = milvus_client.prepare_index_params()
    index_params.add_index(
        field_name="vector_data",
        index_type="IVF_FLAT",
        metric_type="COSINE",
        params={"nlist": 128}
    )

    milvus_client.create_collection(collection_name="CAR_AGENT", schema=schema, index_params=index_params)

    print("milvus_client create collection is ready")


# 数据存
def to_embedding(file_path:str):
    insert_data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f).get('result').get('serieslist')
        if isinstance(data, list) and len(data) > 0:
            for item in data:
                response = embedding_client.embeddings.create(input=item.get('detail'), model=conf.embedding_model,
                                                              dimensions=conf.embedding_dim)
                embedding_text = response.data[0].embedding
                row_data = {
                    "Time": time.time(),
                    "name": item.get('seriesname'),
                    "price": item.get('askprice'),
                    "description": item.get('detail'),
                    "vector_data": embedding_text,
                }
                print(f"{item.get('seriesname')} embedding is ready")
                insert_data.append(row_data)

    return insert_data


if __name__ == '__main__':
    file_path = "C:\\Users\\李涛\\Desktop\\linshi\\car.json"
    #build_milvus()
    insert_data = to_embedding(file_path)
    if len(insert_data) > 0:
        milvus_client.insert(collection_name="CAR_AGENT", data=insert_data)
