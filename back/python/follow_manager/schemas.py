from datetime import datetime

from pydantic import BaseModel


class FollowData(BaseModel):
    followsId: str


class UserCardData(BaseModel):
    id: str
    username: str
    displayName: str
    icon: str
    roles: int
    ratingAvg: float
    isFollowing: bool | None
    isFollowedBy: bool | None
    updatedAt: datetime
    createdAt: datetime


class FollowResponse(BaseModel):
    following: bool
    followed: bool


class FollowersCountData(BaseModel):
    followersCount: int | None = None


class FollowingCountData(BaseModel):
    followingCount: int | None = None


class FollowersCardsData(BaseModel):
    followers: list[UserCardData] | None = None


class FollowingCardsData(BaseModel):
    following: list[UserCardData] | None = None


class UserCardRequestData(BaseModel):
    ids: list[str] | None = None


class UserCardResponseData(BaseModel):
    cards: list[UserCardData]
