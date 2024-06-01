from pydantic import BaseModel


class UsernameChange(BaseModel):
    username: str
    token: str


class TokenValidatorRequestResponse(BaseModel):
    userId: str
    userRoles: int | None
    tokenType: str
