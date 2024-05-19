from constants import ErrorCodes


class RecipeException(Exception):
    def __init__(self, status_code: int, error_code: ErrorCodes):
        super().__init__()
        self.status_code = status_code
        self.error_code = error_code


class UserRetrieverException(Exception):
    def __init__(self, status_code: int, error_code: ErrorCodes):
        super().__init__()
        self.status_code = status_code
        self.error_code = error_code
