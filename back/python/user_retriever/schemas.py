from datetime import datetime

from pydantic import BaseModel


class UserData(BaseModel):
    id: str
    username: str
    displayName: str
    icon: str
    roles: int
    ratingAvg: float
    description: str
    recipes: list[str]
    ratings: list[str]
    updatedAt: datetime
    createdAt: datetime
    followsCount: int
    followersCount: int
    isFollowing: bool | None = None
    isFollowedBy: bool | None = None


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


class UserCardDataList(BaseModel):
    cards: list[UserCardData]


class UserFullData(BaseModel):
    id: str
    username: str
    displayName: str
    icon: str
    roles: int
    ratingAvg: float
    description: str
    recipes: list[str]
    ratings: list[str]
    email: str
    followsCount: int
    followersCount: int
    allergens: list[str]
    searchHistory: list[str]
    messageHistory: list[str]
    savedRecipes: list[str]
    updatedAt: datetime
    createdAt: datetime


class UserCardsRequestData(BaseModel):
    ids: list[str]


class FollowResponse(BaseModel):
    following: bool
    followed: bool

