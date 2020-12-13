from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from fastapi import Query


class OrmModeBaseModel(BaseModel):
    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    nick_name: Optional[str]


class UserResp(OrmModeBaseModel):
    id: int
    username: str
    nick_name: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


page = Query(1, gt=0)
size = Query(10, gt=4, lt=100)
search = Query(None, max_length=32)
ordering = Query(None, max_length=32)

