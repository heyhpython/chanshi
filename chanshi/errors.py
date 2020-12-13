class BaseResponseError(Exception):
    code = None
    message = ""

    def __init__(self, code=None, message=None):
        if code is not None:
            self.code = code
        if message is not None:
            self.message = message
