class RecipeSaverException(Exception):
    def __init__(self, error_code: int):
        super().__init__()
        self.error_code = error_code