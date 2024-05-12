from constants import ErrorCodes


class ImageStorageException(Exception):
    def __init__(self, error_code: ErrorCodes, status_code: int):
        super().__init__()
        self.error_code = error_code
        self.status_code = status_code
