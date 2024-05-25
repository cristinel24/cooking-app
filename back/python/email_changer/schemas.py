from pydantic import BaseModel


class EmailChange(BaseModel):
    email: str
    token: str


class TokenGeneratorRequestResponse(BaseModel):
    value: str
    userId: str
    tokenType: str


class TokenValidatorRequestResponse(BaseModel):
    userId: str
    userRoles: int | None
    tokenType: str
