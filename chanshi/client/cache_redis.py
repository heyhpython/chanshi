from redis import StrictRedis, ConnectionPool


class RedisCache(object):

    def __init__(self):
        self._conn = None

    def init_app(self, app):
        pool = ConnectionPool.from_url(app.config['CACHE_REDIS_URL'])
        self._conn = StrictRedis(connection_pool=pool)

    def __getattr__(self, item):
        return getattr(self._conn, item)
