from flask_cache import Cache

from chanshi.signals import booting
from chanshi.mixins import SQLAlchemy
from chanshi.client.cache_redis import RedisCache

db = SQLAlchemy()
cache = Cache(with_jinja2_ext=False)
redis_cache = RedisCache()


@booting.connect
def init_app(app):
    db.init_app(app)
    cache.init_app(app)
    cache.app = app
    redis_cache.init_app(app)
