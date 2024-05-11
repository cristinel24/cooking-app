from constants import ErrorCodes


class ImageStorageException(Exception):
    def __init__(self, error_code: ErrorCodes):
        super().__init__()
        self.error_code = error_code
