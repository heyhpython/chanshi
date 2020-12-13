from chanshi.signals import booting


@booting.connect
def init_app(app):
    """register api"""
    from .api import api
    app.include_router(
        api,
        prefix="/users",
        tags=["user"]
    )
