class RecipeSaverException(Exception):
    def __init__(self, status_code: int, error_code: int):
        super().__init__()
        self.error_code = error_code
