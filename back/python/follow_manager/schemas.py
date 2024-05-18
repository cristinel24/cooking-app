from pydantic import BaseModel


class FollowData(BaseModel):
    followsId: str


class UserCardData(BaseModel):
    id: str
    username: str
    displayName: str | None = None
    icon: str | None = None
    roles: int | None = None
    ratingAvg: float | None = None


class FollowersCountData(BaseModel):
    followers_count: int | None = None


class FollowingCountData(BaseModel):
    following_count: int | None = None


class FollowersCardsData(BaseModel):
    followers: list[UserCardData] | None = None


class FollowingCardsData(BaseModel):
    following: list[UserCardData] | None = None


class UserCardRequestData(BaseModel):
    ids: list[str] | None = None


class UserCardResponseData(BaseModel):
    cards: list[UserCardData]
