from pydantic import BaseModel, conint
from typing import Optional

import db.mongo_collection


class RecipeData(BaseModel):
    name: str
    title: Optional[str] = None
    description: Optional[str] = None
    prepTime: Optional[int] = None
    steps: Optional[list[str]] = None
    ingredients: Optional[list[str]] = None
    allergens: Optional[list[str]] = None
    tags: Optional[list[str]] = None


class RatingData(BaseModel):
    parent_name: Optional[str]
    recipe_name: str
    rating: conint(ge=0, le=5)
    description: str


class EditRatingData(BaseModel):
    rating_name: str
    rating: conint(ge=0, le=5)
    description: str


class GetRatingsData(BaseModel):
    parent_name: Optional[str]
    start: int
    offset: int
