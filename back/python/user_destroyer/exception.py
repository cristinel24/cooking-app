from constants import ErrorCodes


class UserDestroyerException(Exception):
    def __init__(self, error_code: ErrorCodes, status_code: int):
        self.error_code = error_code
        self.status_code = status_code
