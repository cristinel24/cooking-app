from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class RatingCreate(BaseModel):
    description: str = Field(max_length=10_000)
    rating: int = Field(ge=0, le=5)
    parentType: Literal["recipe", "rating"]
    parentId: str


class UserCardData(BaseModel):
    id: str
    username: str
    displayName: str
    icon: str
    roles: int
    ratingAvg: float
    updatedAt: datetime
    createdAt: datetime


class UserCardDataList(BaseModel):
    cards: list[UserCardData]


class RatingDataCard(BaseModel):
    parentId: str
    parentType: Literal["recipe", "rating"]
    author: UserCardData
    updatedAt: datetime
    createdAt: datetime
    rating: int = Field(0, ge=0, le=5, description="An integer value between 0 and 5")
    description: str
    childrenCount: int
    id: str


class RatingList(BaseModel):
    data: list[RatingDataCard]
    total: int


class RatingUpdate(BaseModel):
    description: str
    rating: int = Field(0, ge=0, le=5, description="An integer value between 0 and 5")
