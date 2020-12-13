from chanshi.signals import booting
from chanshi.mixins import SQLAlchemy

db = SQLAlchemy()


@booting.connect
def init_app(app):
    db.init_app(app)
