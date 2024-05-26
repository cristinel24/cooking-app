from pydantic import BaseModel, Field
from datetime import datetime


class AuthorCardData(BaseModel):
    id: str
    username: str
    displayName: str
    icon: str
    roles: int
    ratingAvg: float
    updatedAt: datetime
    createdAt: datetime


class Rating(BaseModel):
    updatedAt: datetime
    id: str
    authorId: str
    rating: int = Field(0, ge=0, le=5, description="An integer value between 0 and 5")
    description: str
    children: list[str]
    parentId: str
    parentType: str


class RatingChildren(BaseModel):
    children: list[str]
    parentId: str
    parentType: str


class RatingDataCard(BaseModel):
    parentId: str
    parentType: str
    author: AuthorCardData
    updatedAt: str
    rating: int = Field(0, ge=0, le=5, description="An integer value between 0 and 5")
    description: str


class RatingList(BaseModel):
    ratings: list[RatingDataCard]
    total: int


class RatingCreate(BaseModel):
    authorId: str
    description: str
    rating: int = Field(0, ge=0, le=5, description="An integer value between 0 and 5")
    parentType: str


class RatingUpdate(BaseModel):
    description: str
    rating: int = Field(0, ge=0, le=5, description="An integer value between 0 and 5")
