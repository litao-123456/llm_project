from fastapi import APIRouter, Header, HTTPException
from fastapi.params import Cookie
from fastapi.responses import JSONResponse


router = APIRouter()

@router.get("/show")
def read_item():
    data = {
        "message":"peace bride"
    }
    return JSONResponse(data)

@router.get("/items")
# 通过 header 获取数据
def read_items(user_agent:str = Header(None),session_token:str = Cookie(None)):
    return JSONResponse({"user_agent":user_agent,"session_token":session_token})

@router.get("/throw/{item_id}")
def throw_Exception(item_id:int):
    # 自定义抛出异常
    if item_id == 500:
        raise HTTPException(status_code=500,detail="Internal Server Error")
    return {"item_id":item_id}

@router.get("/header/{item_id}")
def throw_Header(item_id:int):
    content = {"user_agent":f"this is {item_id}"}
    headers = {"content-type":"application/json"}
    return JSONResponse(content=content,headers=headers,status_code=200)
