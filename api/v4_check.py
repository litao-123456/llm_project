import time
from typing import Union

from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()

# 依赖项
def time_log(q:str,eq:Union[str:None] = None):
    print(f"向我们走来的是{q},他是来自于：{eq},现在的时间是：{time.time()}")