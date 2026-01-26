from fastapi import APIRouter
from requests import Request
from car_agent import car_lang_garph



router = APIRouter()
@router.post("/car")
async def car_agent(request: Request):
    print(f"car agent request{request.json}")
    await car_lang_garph.car_agent()

    return {"message": "Hello World"}