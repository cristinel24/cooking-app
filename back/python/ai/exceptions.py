import constants


class AIException(Exception):
    def __init__(self, status_code: int, error_code: constants.ErrorCodes | int):
        self.status_code = status_code
        if isinstance(error_code, int):
            self.error_code = error_code
        else:
            self.error_code = error_code.value
