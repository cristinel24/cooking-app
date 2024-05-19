class TokenDestroyerException(Exception):
    def __init__(self, status_code: int, error_code: int):
        self.error_code = error_code
        self.status_code = status_code
