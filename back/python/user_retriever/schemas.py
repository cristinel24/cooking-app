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
    followsCount: int
    following: bool | None = None
    followed: bool | None = None


class UserCardData(BaseModel):
    id: str
    username: str
    displayName: str
    icon: str
    roles: int
    ratingAvg: float
    updatedAt: datetime
    createdAt: datetime
    followsCount: int
    followsCount: int
    following: bool | None = None
    followed: bool | None = None


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
