from pydantic import BaseModel

class TokenData(BaseModel):
    userId: str
    userRoles: int | None = None
    tokenType: str
