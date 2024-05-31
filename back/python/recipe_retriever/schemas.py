from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


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


class RecipeData(BaseModel):
    id: str
    author: UserCardData
    title: str
    description: str
    prepTime: int
    steps: list[str]
    ingredients: list[str]
    allergens: list[str]
    tags: list[str]
    thumbnail: str
    viewCount: int
    userRating: RatingDataCard | None
    isFavorite: bool | None
    ratingAvg: float
    updatedAt: datetime
    createdAt: datetime


class RecipeCardData(BaseModel):
    id: str
    author: UserCardData
    title: str
    description: str
    prepTime: int
    tags: list[str]
    allergens: list[str]
    thumbnail: str
    viewCount: int
    ratingAvg: float
    updatedAt: datetime
    createdAt: datetime
    userRating: RatingDataCard | None
    isFavorite: bool | None
      

class RecipeCardsRequest(BaseModel):
    ids: list[str]


class RecipeCardsResponse(BaseModel):
    recipeCards: list[RecipeCardData | None]


class UserCardRequestData(BaseModel):
    ids: list[str] | None = None


class UserCardResponseData(BaseModel):
    cards: list[UserCardData]
