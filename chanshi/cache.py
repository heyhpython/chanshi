from functools import wraps
import logging
import hashlib

from flask import request


logger = logging.getLogger(__name__)


def make_cache_name(func_name: str):
    try:
        return f'{request.path}-{func_name}'
    except RuntimeError:
        return func_name


def memoize_web_client(timeout=None, unless=None, forced_update=None):
    from chanshi.ext import cache

    def memoize(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            # 注册被装饰的函数
            self.cached_funcs[f.__name__] = f
            func = cache.memoize(timeout=timeout,
                                 make_name=make_cache_name,
                                 unless=unless,
                                 forced_update=forced_update,
                                 hash_method=hashlib.md5)(f)
            return func(self, *args, **kwargs)

        return wrapper

    return memoize


def clear_web_client_cache(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        # 清除 web client 的缓存
        from chanshi.ext import cache
        self.clear_cache(cache)
        return f(self, *args, **kwargs)
    return wrapper
