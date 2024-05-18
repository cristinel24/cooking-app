from pydantic import BaseModel, EmailStr


class UserCreateData(BaseModel):
    username: str
    email: EmailStr
    password: str
    display_name: str = None


class HasherResponse(BaseModel):
    hash: str
    salt: str | None


class TokenResponse(BaseModel):
    value: str
    createdAt: str
    userId: str
    tokenType: str


USER_PROJECTION = {
    "id": 1,
    "register": 1
}
