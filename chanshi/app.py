import time
import logging

from chanshi.mixins import Application
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from flask_migrate import Migrate

from chanshi.signals import booting
from chanshi import ext
from chanshi.utils import init_config


app = Application('chanshi')
init_config(app)
# 跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(filename)s [line:%(lineno)s]  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%SS'
)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def after_request(req: Request, call_nxt):
    start_time = time.time()
    response = await call_nxt(req)
    process_time = time.time() - start_time
    logger.error(f'{req.method}: {req.url} duration {process_time * 1000 // 1 } ms')
    return response


@app.get('/')
def index():
    return 'ok'


booting.send(app)
Migrate(app, ext.db)
