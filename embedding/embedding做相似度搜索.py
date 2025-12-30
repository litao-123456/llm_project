import sys

import pandas as pd
import numpy as np
import ast
from openai import OpenAI

def get_embedding(text):
    # 定义model
    embedding_model = "text-embedding-v4"
    # 维度
    dimensions = 1024
    # 定义 api key
    client = OpenAI(
        api_key="sk-6f65e37d8d0e4e9d9d5c81431ef50522",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    embedding_data = client.embeddings.create(model=embedding_model, input=text, dimensions=dimensions).model_dump()
    if isinstance(embedding_data, dict):
        return embedding_data.get("data")[0].get("embedding")
    return ""


pf = pd.read_csv("data/embedding_output_1k.csv", index_col=0)

# 转换矩阵
pf['embedding_vec'] = pf['embedding_data'].apply(ast.literal_eval)


# 计算余弦相似度， -1、0、1 三个维度表示
# -1 两个相关
# 1 很接近
# 0 表示中立，接近垂直
def confine_distance(a, b):
    # 两个向量的之间的余弦夹角值
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# 搜索
def search_word(df, word, topK, print_flage=True):

    word_embedding = get_embedding(word)
    # 两个进行对比
    df['compare_data'] = df['embedding_vec'].apply(lambda x:confine_distance(x, word_embedding))
    df.to_csv("data/embedding_output_2k.csv", index=False)
    # 通过余弦向量排序，取TpoK 条
    res = (
        df.sort_values('compare_data', ascending=False)
        .head(topK)
    )
    for index, row in res.iterrows():
        if print_flage:
            print(f"余弦相似度：{row['compare_data']} 评论内容：{row['combined']} ")
    return None


if __name__ == '__main__':
    search_word(pf, "bad",3)