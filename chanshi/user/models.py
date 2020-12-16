from chanshi.ext import db
from chanshi.mixins import BasicMixin


class User(db.Model, BasicMixin):
    """
    铲屎用户模型，铲屎任务的发布方或者铲屎任务执行方
    """
    search_fields = ('username', 'nick_name')

    username = db.Column(db.String(64), index=True, unique=True)
    nick_name = db.Column(db.String(64), index=True, unique=True, comment='微信的用户昵称')
    openid = db.Column(db.String(64), index=True, unique=True, comment='用户唯一标识')
    unionid = db.Column(db.String(64), index=True, unique=True, comment='开放平台唯一id')
    mobile = db.Column(db.Integer, index=True, comment='手机号')
    avatar = db.Column(db.TEXT, comment='头像地址')
    gender = db.Column(db.SMALLINT, comment='用户性别', default=0)
