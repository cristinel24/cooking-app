from pydantic import BaseModel, conint
from typing import Optional


class RecipeData(BaseModel):
    title: str
    description: str
    prep_time: conint(ge=0, le=2 ** 31 - 1)
    steps: str
    ingredients: str
    allergens: str
    tags: str


class RatingData(BaseModel):
    parent_name: str[Optional]
    recipe_name: str
    rating: conint(ge=0, le=5)
    description: str


class EditRatingData(BaseModel):
    rating_name: str
    rating: conint(ge=0, le=5)
    description: str


class GetRatingsData(BaseModel):
    parent_name: str[Optional]
    start: int
    offset: int
