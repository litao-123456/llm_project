# database.py
from contextlib import contextmanager
import pymysql
import redis
from config import settings

class Database:
    def __init__(self):
        self.mysql_config = {
            "host": settings.MYSQL_HOST,
            "port": settings.MYSQL_PORT,
            "user": settings.MYSQL_USER,
            "password": settings.MYSQL_PASSWORD,
            "database": settings.MYSQL_DATABASE,
            "charset": "utf8mb4",
            "autocommit": False,
            "connect_timeout": 10,
        }
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
        )

    @contextmanager
    def mysql_connection(self):
        """提供带自动关闭的数据库连接"""
        conn = None
        try:
            conn = pymysql.connect(**self.mysql_config)
            print("mysql connect ok")
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn and conn.open:
                conn.close()

    def get_redis(self):
        return self.redis_client

# 全局单例（模块级）
db = Database()