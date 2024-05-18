from pydantic import BaseModel, Field
from typing import Optional


class RatingBase(BaseModel):
    description: str
    rating: int = Field(..., ge=1, le=5)  # Ensure rating is within [1, 5]


class CreateRating(RatingBase):
    authorId: str


class UpdateRating(BaseModel):
    description: Optional[str] = None
    rating: Optional[int] = Field(None, ge=0, le=5)  # Ensure rating is within [0, 5]


class RatingResponse(BaseModel):
    id: str
    recipe_id: str
    author_id: str
    description: str
    rating: int

class RatingRequest(BaseModel):
    authorId: str
    description: str
    rating: int


USER_PROJECTION = {
    "id": 1,
    "ratingSum": 1,
    "ratingCount": 1
}

RECIPE_PROJECTION = {
    "id": 1,
    "ratingSum": 1,
    "ratingCount": 1
}

