from requests import Request
import asyncio
from fastapi import APIRouter
from langchain.agents import create_agent

router = APIRouter()

"""
"""

async def car_agent(request: Request):
    request = await request.json()
    print(f"car agent request{request}")

async def langchain_agent(request: Request):
    request = await request.json()
    print(request)







