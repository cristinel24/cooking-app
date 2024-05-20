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
        if recipe_data.title is not None:
            self.title = recipe_data.title
        if recipe_data.description is not None:
            self.description = recipe_data.description
        if recipe_data.prepTime is not None:
            self.prepTime = recipe_data.prepTime
        if recipe_data.steps is not None:
            self.steps = recipe_data.steps
        if recipe_data.ingredients is not None:
            self.ingredients = recipe_data.ingredients
        if recipe_data.allergens is not None:
            self.allergens = recipe_data.allergens
        if recipe_data.tags is not None:
            self.tags = recipe_data.tags
        if recipe_data.thumbnail is not None:
            self.thumbnail = recipe_data.thumbnail
