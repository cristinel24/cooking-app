from pydantic import BaseModel


class TokenData(BaseModel):
    value: str
    userId: str
    tokenType: str
