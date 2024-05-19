import datetime

from pydantic import BaseModel
from typing import Optional


class RecipeData(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    prepTime: Optional[int] = None
    steps: Optional[list[str]] = None
    ingredients: Optional[list[str]] = None
    allergens: Optional[list[str]] = None
    tags: Optional[list[str]] = None
    thumbnail: Optional[str] = None


class Recipe:
    def __init__(self, recipe_data: RecipeData):
        TODO: validations
        self.title = recipe_data.title
        self.description = recipe_data.description
        self.prepTime = recipe_data.prepTime
        self.steps = recipe_data.steps
        self.ingredients = recipe_data.ingredients
        self.allergens = recipe_data.allergens
        self.tags = recipe_data.tags
        self.thumbnail = recipe_data.thumbnail
