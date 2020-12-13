import os
import re
import logging
from typing import Any
from datetime import datetime

from fastapi import FastAPI, encoders

from flask.config import Config
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import DATETIME, Column, Integer, text, or_
from pydantic import BaseModel
from sqlalchemy.inspection import inspect

logger = logging.getLogger(__name__)


def get_env():
    return os.environ.get("FASTAPI_ENV") or "production"


class Application(FastAPI):
    """
    fastApi APP support init_app like flask
    """
    config_class = Config
    extensions = {}
    teardown_appcontext_funcs = []

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.import_name = name
        self.config = self.make_config()

    def make_config(self):
        root_path = self.root_path
        defaults = dict()
        defaults["ENV"] = get_env()
        return self.config_class(root_path, defaults)

    def teardown_appcontext(self, f):
        self.teardown_appcontext_funcs.append(f)
        return f


class SQLAlchemy(_SQLAlchemy):

    def init_app(self, app):
        super().init_app(app)
        self.app = app

    def get_app(self, reference_app=None):
        return self.app


class BasicMixin(object):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DATETIME, server_default=text('NOW()'), nullable=False, index=True)
    updated_at = Column(DATETIME, server_default=text('NOW()'), onupdate=text('NOW()'), nullable=False, index=True)

    @classmethod
    def find_or_create(cls, **kwargs):
        if kwargs:
            item = cls.query.filter_by(**kwargs).first()
            if item is None:
                item = cls(**kwargs)
            return item
        raise ValueError("parameter is empty!")

    @classmethod
    def create(cls, **kwargs):
        item = cls(**kwargs)
        return item

    @staticmethod
    def pagination_dump(
            query, page, size, dump_method=lambda x: x.to_dict()
    ) -> dict:
        pagination = query.paginate(
            page=page, per_page=size, error_out=False
        )

        return dict(
            pagination=dict(
                page=pagination.page,
                size=pagination.per_page,
                pages=pagination.pages,
                total=pagination.total,
                has_next=pagination.has_next,
                has_prev=pagination.has_prev
            ),
            data=[dump_method(i) for i in pagination.items]
        )

    def to_dict(self, **kwargs):
        data = {}
        for col in self.__table__.columns:
            val = getattr(self, col.name)
            if isinstance(val, datetime):
                val = val.isoformat()
            data[col.name] = val
        return data


def get_ordering_field(ordering):
    if not ordering:
        return None, None
    ordering = ordering.strip()
    match = re.match(r'^([+|-]?)(\S+)$', ordering)
    if not match:
        return None, None
    ret = match.groups()
    return ret[0] or '+', ret[1]


def get_column(field, object_cls):
    if not field:
        return None
    fields = field.split('.')
    if len(fields) == 1:
        cls = object_cls
        field_name = field
    else:
        start = object_cls
        for x in fields[:-1]:
            relations = inspect(start).relationships
            prop = relations.get(x)
            start = prop.entity
        cls = getattr(start, 'class_', None) or start
        field_name = fields[-1]
    return getattr(cls, field_name)


def get_ordering_func(ordering, object_cls):
    try:
        direction, field = get_ordering_field(ordering)
        column = get_column(field, object_cls)
        func_name = 'desc' if direction == '-' else 'asc'
        return getattr(column, func_name, None)
    except Exception as ex:
        logger.exception(ex)
        return None


class PaginationMixin:

    @classmethod
    def get_pagination(cls, object_cls, db_query, search_fields=(), order_by_func=None, args: dict = None):  # noqa
        if isinstance(args, dict):
            page, page_size, ordering, search = \
                args['page'], args['size'], args['ordering'], args['search']
        else:
            page, page_size, ordering, search = 1, 10, None, None
        if search:
            db_query = db_query.filter(cls._make_search(search, search_fields, object_cls))  # noqa
        if callable(order_by_func):
            db_query = db_query.order_by(None).order_by(order_by_func())
        elif ordering:
            func = get_ordering_func(ordering, object_cls)
            if callable(func):
                db_query = db_query.order_by(None).order_by(func())
        return db_query.paginate(page=page, per_page=page_size)

    @classmethod
    def _make_search(cls, search, search_fields, object_cls):
        search = cls._escape(search)
        conditions = []
        for c in search_fields:
            try:
                if isinstance(c, str):
                    column = get_column(c, object_cls)
                else:
                    column = c
                func = getattr(column, 'contains', None)
                if callable(func):
                    conditions.append(func(search))
            except Exception as ex:
                logger.exception(ex)
        return or_(*conditions)

    @staticmethod
    def _escape(search):
        if not search:
            return search
        return search.replace('%', '\\%').replace('_', '\\_')

    @staticmethod
    def dump_pagination(pagination):
        return dict(
            page=pagination.page,
            size=pagination.per_page,
            pages=pagination.pages,
            total=pagination.total,
            has_next=pagination.has_next,
            has_prev=pagination.has_prev
        )


def model_iter(instances, *annotated_fields):
    """
    实现类似Django annotate功能
    将select出来的额外列添加到 model instance 里面
    注意annotated_fields需要与select的顺序一致
    """
    for i in instances:
        ret = i
        if isinstance(i, tuple):
            ret = i[0]
            data = ret.to_dict()
            for idx, field in enumerate(annotated_fields):
                if isinstance(field, str):
                    name, type_ = field, str
                else:
                    name, type_ = field['name'], field['type']
                original_value = i[idx + 1]
                value = type_(original_value) if original_value is not None else None  # noqa
                # setattr(ret, name, value)
                data[name] = value
            yield data
        else:
            yield ret
