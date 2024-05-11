from fastapi import HTTPException

class CustomException(HTTPException):
    def __init__(self, status_code: int = 500, detail: str = "Internal Server Error", headers: dict = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
