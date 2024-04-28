class BaseCustomException(Exception):
    def __init__(self, detail):
        self.detail = detail
        super().__init__(self.detail)


class ExternalAPIException(BaseCustomException): ...


class DBException(BaseCustomException): ...
