from functools import lru_cache

from chanshi.client.web_client import WebClient
from chanshi.errors import WeChatError


class WeChatClient(WebClient):
    SECRET = None
    APPID = None

    def get_name(self):
        return "WECHAT"

    def init_app(self, app):
        super().init_app(app)
        self.SECRET = app.config['WECHAT_APPSECRET']
        self.APPID = app.config['WECHAT_APPID']

    def get_access_token(self, appid, secret):
        resp = self.get(
            'cgi-bin/token',
            grant_type='client_credential',
            appid=self.APPID,
            secret=self.SECRET
        )
        if resp['errcode'] != 0:
            raise WeChatError(message=resp['errmsg'])
        return resp['access_token']

    def get_paid_union_id(self, transaction_id):
        """根据微信支付订单号获取union_id
        调用前需要用户完成支付，且在支付后的五分钟内有效。
        """
        resp = self.get(
            'wxa/getpaidunionid',
            access_token=self.get_wechat_access_token(),
            openid='OPENID',
            transaction_id=transaction_id
        )
        return resp['unionid']

    @lru_cache(maxsize=100)
    def get_wechat_access_token(self):
        return self.get_access_token()

    def code_2_session(self, code):
        resp = self.get(
            'sns/jscode2session',
            appid=self.APPID, secret=self.SECRET,
            js_code=code, grant_type='authorization_code'
        )
        if resp['errcode'] != 0:
            raise WeChatError(message=resp['errmsg'])
        return resp
