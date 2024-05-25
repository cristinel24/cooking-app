from pydantic import BaseModel


class LoginData(BaseModel):
    identifier: str
    password: str


class HasherResponse(BaseModel):
    hash: str
    salt: str | None


class TokenResponse(BaseModel):
    value: str
    userId: str
    tokenType: str


class UserCardData(BaseModel):
    id: str
    username: str
    displayName: str
    icon: str
    roles: int
    ratingAvg: float
    # isFollowing: bool
    # isFollowed: bool
    # followsCount: int
    # followersCount: int


class LoginResponse(BaseModel):
    sessionToken: str
    user: UserCardData
