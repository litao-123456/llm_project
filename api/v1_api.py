import json

from fastapi import APIRouter
from starlette.responses import JSONResponse

from database import db
from pymysql.cursors import DictCursor

from models.tb_teacher import TbSubject


router = APIRouter()


@router.get("/get/{version}")
def show_v1(version: str):
    sql_str = """
              SELECT *
              FROM tb_subject where no = %s \
              """
    with db.mysql_connection() as con:
        cursor = con.cursor(DictCursor)
        cursor.execute(sql_str,version)
        result = cursor.fetchone()
        if result:
            return TbSubject(**result)
        return None


@router.post("/create_subject")
def create_subject(subject: TbSubject):
    print("create subject")
    sql_str = """
              INSERT INTO tb_subject(no, name, intro, is_hot)
              VALUES (%s, %s, %s, %s) \
              """
    with db.mysql_connection() as con:
        cursor = con.cursor(DictCursor)
        cursor.execute(sql_str, (subject.no, subject.name, subject.intro, subject.is_hot))
        con.commit()
    redis = db.get_redis()
    # redis 不能直接存储 pydantic类型数据，需要把他序列化成字符串
    redis.set("redis_client", subject.model_dump_json())
    return subject


@router.get("/show_list")
def show_list():
    print("show list")
    sql_query = """
                SELECT *
                FROM tb_subject \
                """
    subject_list = []
    with db.mysql_connection() as con:
        cursor = con.cursor(DictCursor)
        cursor.execute(sql_query)
        result = cursor.fetchall()
        for _ in result:
            subject_list.append(_)
    return JSONResponse({"data": subject_list})


@router.get("/llm/{query}")
def show_llm(query: str):
    from fastapi.responses import StreamingResponse
    from langchain_demo.langchain_demo import SimpleChainServices
    return StreamingResponse(SimpleChainServices.create_simple_chains(query),
                             media_type="text/event-stream",
                             headers={
                                 "Cache-Control": "no-cache",
                                 "Connection": "keep-alive",
                                 "Access-Control-Allow-Origin": "*",
                                 "Access-Control-Allow-Headers": "*",
                             }
                             )
