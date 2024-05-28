from datetime import datetime

from pydantic import BaseModel


class UserCardData(BaseModel):
    id: str
    username: str
    displayName: str
    icon: str
    roles: int
    ratingAvg: float
    updatedAt: datetime
    createdAt: datetime


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


class RecipeCardsRequest(BaseModel):
    ids: list[str]


class RecipeCardsResponse(BaseModel):
    recipeCards: list[RecipeCardData | None]


class UserCardRequestData(BaseModel):
    ids: list[str] | None = None


class UserCardResponseData(BaseModel):
    cards: list[UserCardData]
