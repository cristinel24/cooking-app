class LoginException(Exception):
    def __init__(self, error_code: int, http_code: int):
        super().__init__()
        self.error_code = error_code
        self.http_code = http_code
