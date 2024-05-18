from pydantic import BaseModel

class TokenData(BaseModel):
    userId: str
    userRoles: int
    tokenType: str
