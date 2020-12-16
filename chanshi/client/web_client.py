import logging
from abc import abstractmethod
import time

import requests

from chanshi.cache import clear_web_client_cache
from chanshi.errors import NotFoundError


logger = logging.getLogger(__name__)


class Session(requests.Session):

    def request(self, method: str, url, *args, **kwargs):
        s = time.time()
        resp = super(Session, self).request(method, url, *args, **kwargs)
        logger.info(f"{method} {url} args:{args} kwargs:{kwargs} "
                    f"status:{resp.status_code} "
                    f"cost: {int((time.time()-s) * 1000)} ms")
        return resp


class WebClient:
    cached_funcs = {}

    def __init__(self, auth_header=None, token_prefix=None, env=None):
        self.session = Session()
        self.auth_header = auth_header or 'Authorization'
        self.token_prefix = token_prefix or "Bearer "
        self.env = env
        self.endpoint = None
        self.token = None

    def init_app(self, app):
        self.endpoint = app.config[self.endpoint_config_name].rstrip("/")
        self.token = app.config[self.token_config_name]

        self.session.headers[self.auth_header] = "{}{}".format(
            self.token_prefix, self.token
        )

    def update_config(self, app):
        self.init_app(app)

    @abstractmethod
    def get_name(self):
        """please implement in subclass"""

    @property
    def name(self):
        return self.get_name()

    @property
    def endpoint_config_name(self):
        if self.env is None:
            return f"{self.name}_API_ENDPOINT"
        else:
            env = self.env.upper()
            return f"{env}_{self.name}_API_ENDPOINT"

    @property
    def token_config_name(self):
        if self.env is None:
            return f"{self.name}_TOKEN"
        else:
            env = self.env.upper()
            return f"{env}_{self.name}_TOKEN"

    def path_join(self, uri):
        return f"{self.endpoint}/{uri}"

    def prepare_request(self, path):
        full_path = self.path_join(path)
        self.session.headers[self.auth_header] = self.token
        return full_path

    def get(self, path, **kwargs):
        full_path = self.prepare_request(path)
        resp = self.session.get(full_path, params=kwargs)
        if resp.status_code == 404:
            logger.warning(
                f"GET from {self.name} not found path: {path} kwargs: {kwargs}"
            )
            raise NotFoundError()
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            return resp.content

    @clear_web_client_cache
    def post(self, path, **kwargs):
        full_path = self.prepare_request(path)
        resp = self.session.post(full_path, **kwargs)
        resp.raise_for_status()
        return resp.json()

    @clear_web_client_cache
    def put(self, path, **kwargs):
        full_path = self.prepare_request(path)
        resp = self.session.put(full_path, **kwargs)
        resp.raise_for_status()
        return resp.json()

    @clear_web_client_cache
    def delete(self, path, **kwargs):
        full_path = self.prepare_request(path)
        resp = self.session.delete(full_path, json=kwargs)
        resp.raise_for_status()
        try:
            return resp.json()
        except ValueError:
            return resp.content

    def clear_cache(self, cache):
        # 清除客户端的缓存, 在资源做出修改之后
        list(map(cache.delete_memoized, self.cached_funcs.values()))
