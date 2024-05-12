from constants import ErrorCodes
from fastapi import status


class ProfileDataChangerException(Exception):
    def __init__(self, status_code: status, error_code: ErrorCodes):
        self.status_code = status_code
        self.error_code = error_code
