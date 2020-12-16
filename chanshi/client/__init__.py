from .wechat import WeChatClient
from chanshi.signals import booting

wechat_client = WeChatClient()


@booting.connect
def init_app(app):
    wechat_client.init_app(app)
