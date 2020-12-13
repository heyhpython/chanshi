import os
import logging

from fastapi import FastAPI
from flask.config import Config
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


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
