import json
import os
import pandas as pd
import tiktoken
from openai import OpenAI

# 读取csv文件，将两个字段合并为一个
df = pd.read_csv("data/fine_food_reviews_1k.csv",index_col=0)

df = df[["Time","ProductId","UserId","Score","Summary","Text"]]

df = df.dropna()

df['combined'] = "Title:" + df.Summary.str.strip() + "; Content:" + df.Text.str.strip()



embedding_model = "text-embedding-v4"

max_token = 8000

# 根据日期进行排序，然后删除掉日期字段
df = df.sort_values('Time')

# 创建分词器进行分词
tokenizer_name = 'cl100k_base'
tokenizer = tiktoken.get_encoding(encoding_name=tokenizer_name)

# 计算token的数量
df['count_token'] = df.combined.apply(lambda x: len(tokenizer.encode(x)))

# 截取1000个，符合小于8191的数据
df = df[df.count_token <= 8191].tail(10)


def get_embedding_template(text,model="text-embedding-v4"):
    client = OpenAI(
        api_key="sk-6f65e37d8d0e4e9d9d5c81431ef50522",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    embedding_data = client.embeddings.create(model=model,input=text,dimensions=1024).model_dump()
    if isinstance(embedding_data,dict):
        print(embedding_data)
        return embedding_data.get("data")[0].get("embedding")
    return None




df["embedding_data"] = df.combined.apply(get_embedding_template)

df.to_csv('data/embedding_output_1k.csv')


def test_embedding(text):
    get_embedding_template(text)


if __name__ == '__main__':
    test_embedding("好久不见，真的好久不见")
