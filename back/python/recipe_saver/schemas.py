from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class UserCardData(BaseModel):
    id: str
    username: str
    displayName: str
    icon: str
    roles: int
    ratingAvg: float
    updatedAt: datetime
    createdAt: datetime
    isFollowing: Optional[bool] = None
    isFollowedBy : Optional[bool] = None


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


class SavedRecipesModel(BaseModel):
    data: list[RecipeCardData]
    total: int


class RecipeCardsRequest(BaseModel):
    ids: list[str]


class RecipeCardsResponse(BaseModel):
    recipeCards: list[RecipeCardData]
