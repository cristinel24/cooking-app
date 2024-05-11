class SearchHistoryException(Exception):
    def __init__(self, error_code: int, message: str):
        super().__init__()
        self.error_code = error_code
        self.message = message
