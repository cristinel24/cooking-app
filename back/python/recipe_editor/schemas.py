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
        for key, value in recipe_data.model_dump().items():
            if value is not None:
                setattr(self, key, value)
