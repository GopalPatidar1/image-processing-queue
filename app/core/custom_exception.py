class CustomException(Exception):
    def __init__(self, status_code: int = 500, message: str | None=None):
        self.status_code = status_code  or 500
        self.message = message or "something went wrong"