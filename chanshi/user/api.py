import logging

from fastapi import APIRouter, Query, Body

from .models import User
from chanshi.user import validators
from chanshi.ext import db
from chanshi.client import wechat_client

api = APIRouter()
logger = logging.getLogger(__name__)


@api.post('/sessions', response_model=validators.SessionOut)
async def create_session(session_in: validators.SessionIn):
    """
    通过微信js_code创建微信的session
    """
    # 1. 通过js_code获取 session_key
    resp = wechat_client.code_2_session(session_in.js_code)
    user = User.find_or_create(openid=resp['openid'], unionid=resp['unionid'])
    db.session.add(user)
    db.session.commit()
    # 2.通过session_key 获取用户信息
    return resp


@api.post('/users/{openid}', response_model=validators.UserResp)
async def update_user(openid=Query(None, description='用户在微信的唯一标识'),
                      user_id: validators.UserIn = Body(None)):
    """
    更新用户信息，前端获取用户信息之后的回调
    """
    user = User.query.filter_by(openid=openid).first_or_404()
    user.update(**user_id.dict(exclude_unset=True))
    return user
