class TokenException(Exception):
    def __init__(self, status_code: int, error_code: int):
        super().__init__()
        self.status_code = status_code
        self.error_code = error_code


class UserException(Exception):
    def __init__(self, status_code: int, error_code: int):
        super().__init__()
        self.status_code = status_code
        self.error_code = error_code
