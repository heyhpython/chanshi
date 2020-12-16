from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from fastapi import Query


class OrmModeBaseModel(BaseModel):
    class Config:
        orm_mode = True


class UserIn(BaseModel):
    username: Optional[str]
    nick_name: Optional[str]
    avatar: Optional[str]
    gender: Optional[int]
    mobile: Optional[str]


class UserResp(OrmModeBaseModel):
    id: int
    username: str
    nick_name: Optional[str]
    openid: str
    unionid: str
    mobile: str
    avatar: Optional[str]
    gender: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


page = Query(1, gt=0)
size = Query(10, gt=4, lt=100)
search = Query(None, max_length=32)
ordering = Query(None, max_length=32)


class SessionIn(BaseModel):
    """创建session入参"""
    js_code: str


class SessionOut(BaseModel):
    """创建session返回"""
    session_key: str
    openid: str
    unionid: str
