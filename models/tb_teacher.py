# coding: utf-8
from typing import Optional
import re

from pydantic import BaseModel, field_validator, model_validator


class TbSubject(BaseModel):
    no: int
    name:Optional[str] = None
    intro: str
    is_hot: int

    @field_validator('name')
    @classmethod
    def check_name(cls, v):
        print("运行了此代码......")
        if v is None:
            raise ValueError("name is not None")
        if not v.strip():
            raise ValueError("名称不能为空")
        return v.strip()

    @model_validator(mode='after')
    def check_intro_and_name(self):
        check_str = ['傻','逼']
        if any(check in self.name for check in check_str):
            raise ValueError("含有非法字符")
        if not self.intro.strip():
            raise ValueError("名称不能为空")

        return self



