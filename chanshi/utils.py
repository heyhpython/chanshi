import os
import logging

from chanshi.constants import __config__


logger = logging.getLogger(__name__)


def init_config(app):
    load_config(app)


def load_config(app):
    if os.path.isfile(__config__):
        app.config.from_pyfile(__config__)
        app.config["DEBUG"] = True
        logger.warning("using local config file".center(50, "#"))
        return None
    else:
        pass
