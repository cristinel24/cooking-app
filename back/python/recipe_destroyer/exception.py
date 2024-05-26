from constants import ErrorCodes


class RecipeDestroyerException(Exception):
    error_code: int
    status_code: int

    def __init__(self, error_code: int | ErrorCodes, status_code: int):
        super().__init__()
        self.status_code = status_code
        if isinstance(error_code, ErrorCodes):
            self.error_code = error_code.value
        else:
            self.error_code = error_code

    def __repr__(self):
        return f"RecipeDestroyerException(status_code={self.status_code}, error_code={self.error_code})"
