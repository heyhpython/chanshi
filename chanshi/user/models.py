from chanshi.ext import db
from chanshi.mixins import BasicMixin


class User(db.Model, BasicMixin):
    """
    铲屎用户模型，铲屎任务的发布方或者铲屎任务执行方
    """
    search_fields = ('username', 'nick_name')

    username = db.Column(db.String(64), index=True, unique=True)
    nick_name = db.Column(db.String(64), index=True, unique=True)
