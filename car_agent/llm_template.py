import os
from env.config import conf
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_milvus import Milvus
from car_agent.embeddings import qwen_embedding
#
class _LLMTemplate:

    def __init__(self):

        self.car_agent_milvus = Milvus(
            embedding_function=qwen_embedding,
            connection_args={"uri":conf.milvus_client_url},
            collection_name="CAR_AGENT",
            text_field="description",
            vector_field="vector_data",
        )
        print("car_agent_milvus  -- is  ready")

        # llm
        self.qwen_plus = ChatOpenAI(
            model="qwen-plus",
            api_key=conf.qianwen_api_key,
            base_url=conf.qianwen_llm_url,
            temperature=0.5
        )

        print("qwen_plus  -- is  ready")

        # 向量化
        self.qwen_embedding = OpenAIEmbeddings(
            model="qwen-embedding",
            api_key=conf.embedding_api_key,
            base_url=conf.embedding_url,
            dimensions=256
        )
        print("qwen_embedding  -- is  ready")



init_client = _LLMTemplate()