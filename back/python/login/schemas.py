from pydantic import BaseModel


class State(BaseModel):
    user_id: str
    user_roles: int


class LoginData(BaseModel):
    state: State
    identifier: str
    password: str


class HasherResponse(BaseModel):
    hash: str
    salt: str | None


class TokenResponse(BaseModel):
    value: str
    userId: str
    tokenType: str


class LoginResponse(BaseModel):
    sessionToken: str
