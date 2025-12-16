from time import sleep

# 今日任务，搭建现代版 FastAPI
# 通过依赖引入mysql,redis,mervis
# 封装接口，操作各DB

from pydantic import BaseModel

class Teacher(BaseModel):
    no: int
    name: str
    sex:str
    birth:str
    intro:str

async def yield_test():
    for i in range(10):
        yield i
        print(i)


if __name__ == '__main__':
    yield_test()

