from datetime import datetime

from pydantic import BaseModel, Field


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
    createdAt: datetime
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
    updatedAt: datetime
    createdAt: datetime
    rating: int = Field(0, ge=0, le=5, description="An integer value between 0 and 5")
    description: str
    childrenCount: int


async def card_from_rating(rating: Rating) -> RatingDataCard:
    from api import ExternalDataProvider

    return RatingDataCard(
        parentId=rating.parentId,
        parentType=rating.parentType,
        author=await ExternalDataProvider().get_user(rating.authorId),
        updatedAt=rating.updatedAt,
        createdAt=rating.createdAt,
        rating=rating.rating if rating.parentType == "recipe" else 0,
        description=rating.description,
        childrenCount=len(rating.children)
    )


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
