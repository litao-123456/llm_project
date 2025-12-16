from typing import Union

from fastapi import FastAPI

from api.pydantic_test import BaseModel

from api.v1_api import router as v1_router
from api.pydantic_test import router as v2_router
from api.v3_http import router as v3_router
app = FastAPI() # 引用实例 是主路由，
app.include_router(v1_router,prefix="/v1") # router 是局部路由，其他路由，通过挂载到主应用上才能注册访问
app.include_router(v2_router,prefix="/v2")
app.include_router(v3_router,prefix="/v3")


class Item(BaseModel):
    name: str
    price: float
    quantity: int


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# q:Union[str,None] = None 表示q 可以不传，或者可以为空
@app.get("/query_page/{name}")
async def query_page(name: str,q:Union[str,None] = None):
    return {"message": f"Hello {name},q:{q}"}

@app.put("/update_page/{name}")
async def update_page(name:str,item:Item):
    return {"message": f"Hello {name},q:{item.name},q:{item.quantity}"}
