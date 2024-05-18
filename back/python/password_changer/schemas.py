from pydantic import BaseModel


class PasswordChange(BaseModel):
    password: str
    token: str


class PasswordHashRequestResponse(BaseModel):
    hashAlgorithmName: str
    hash: str
    salt: str
