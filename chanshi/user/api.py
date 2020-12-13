import logging
from typing import Optional

from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError

from .models import User
from chanshi.mixins import PaginationMixin
from chanshi.user import validators
from chanshi.ext import db
from chanshi.errors import BaseResponseError

api = APIRouter()
logger = logging.getLogger(__name__)


@api.get('/')
async def users_api(
        page: Optional[int] = validators.page, size: Optional[int] = validators.size,
        search: Optional[str] = validators.search, ordering: Optional[str] = validators.ordering):
    query = User.query
    pagination = PaginationMixin.get_pagination(
        User, query, search_fields=User.search_fields,
        args={"page": page, "size": size, "search": search, "ordering": ordering}

    )
    return {
        "data": pagination.items,
        "pagination": PaginationMixin.dump_pagination(pagination)
    }


@api.post('/', response_class=validators.UserResp)
async def users_api(user: validators.User):
    user = User(**user.dict())
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        logger.error(e)
        raise BaseResponseError(code=400, message='用户名重复')
    logger.error(user)
    return user.to_dict()


@api.get('/{user_id}', response_model=validators.UserResp)
async def user_api(user_id):
    user = User.query.get(user_id)
    return user
