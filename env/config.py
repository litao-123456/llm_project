import os
from dotenv import load_dotenv

# 模块化单例模式
class _Config:
    def __init__(self):
        file_path = os.path.dirname(__file__)

        active_profile = os.getenv("ACTIVE_PROFILE","")
        if active_profile == "dev":
            env_file = os.path.join(file_path, ".env-dev")
        else:
            env_file = os.path.join(file_path, ".env-local")

        print(f"active profile: {active_profile}")
        load_dotenv(dotenv_path=env_file)
        # APP
        self.app_env = os.getenv("APP_ENV", "")

        # MYSQL
        self.mysql_host = os.getenv("MYSQL_HOST", "")
        self.mysql_port = os.getenv("MYSQL_PORT", "")
        self.mysql_user = os.getenv("MYSQL_USER", "")
        self.mysql_password = os.getenv("MYSQL_PASSWORD", "")
        self.mysql_database = os.getenv("MYSQL_DATABASE", "")

        # REDIS
        self.redis_host = os.getenv("REDIS_HOST", "")
        self.redis_port = os.getenv("REDIS_PORT", "")

        # LLM
        self.qianwen_api_key = os.getenv("QIANWEN_API_KEY", "")
        self.qianwen_llm_model = os.getenv("QIANWEN_LLM_MODEL", "")
        self.qianwen_llm_url = os.getenv("QIANWEN_LLM_URL", "")

        # EMBEDDING
        self.embedding_api_key = os.getenv("EMBEDDING_API_KEY", "")
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "")
        self.embedding_url = os.getenv("EMBEDDING_URL", "")
        self.embedding_dim = os.getenv("EMBEDDING_DIM", "")

        # RERANK
        self.rerank_model = os.getenv("RERANK_MODEL", "")
        self.dashscope_api_key = os.getenv("DASHSCOPE_API_KEY", "")
        self.dashscope_rerank_url = os.getenv("DASHSCOPE_RERANK_URL", "")

        # MILVUS
        self.milvus_client_url = os.getenv("MILVUS_CLIENT_URL", "")
        self.milvus_client_user = os.getenv("MILVUS_CLIENT_USER", "")
        self.milvus_client_pwd = os.getenv("MILVUS_CLIENT_PWD", "")

        #WEB_SEARCH
        self.qwen_web_search_url = os.getenv("WEB_SEARCH_URL", "")
        self.qwen_web_search_api_key = os.getenv("WEB_SEARCH_API_KEY", "")


conf = _Config()