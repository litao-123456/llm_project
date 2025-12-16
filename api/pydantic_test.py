from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

class Item(BaseModel):
    name: str
    price: float
    quantity: int

@router.post("/item")
def read_item(item: Item):
    # 直接访问，fastApi 会自动转换成 json
    return item

