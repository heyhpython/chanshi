import time
import logging

from chanshi.mixins import Application
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from chanshi.utils import init_config
from chanshi.signals import booting
from chanshi import user  # noqa
from chanshi import ext  # noqa
from chanshi.errors import BaseResponseError

app = Application('chanshi')
init_config(app)
booting.send(app)

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


@app.exception_handler(500)
async def handle_exception(req, exc):
    logger.error(exc)
    return JSONResponse(
        status_code=500,
        content=dict(
            code=500,
            message=str(exc)
        )
    )


@app.exception_handler(BaseResponseError)
async def handle_exception(req, exc):
    logger.error(exc)
    return JSONResponse(
        status_code=exc.code,
        content=dict(
            code=exc.code,
            message=exc.message
        )
    )


@app.get('/')
def index():
    return 'ok'
