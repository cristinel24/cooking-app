from pydantic import BaseModel


class PasswordChange(BaseModel):
    password: str
    token: str


class HasherRequestResponse(BaseModel):
    hashAlgorithmName: str
    hash: str
    salt: str


class TokenValidatorRequestResponse(BaseModel):
    userId: str
    userRoles: int | None
    tokenType: str
