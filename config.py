# config.py
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    # mysql 配置
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    # Redis 配置 👈 新增
    REDIS_HOST: str
    REDIS_PORT: int

    # 应用环境 👈 新增
    APP_ENV: str = "dev"  # 可设默认值

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    class Config:
        env_file = BASE_DIR / "env" / ".env-dev"
        env_file_encoding = "utf-8"

settings = Settings()