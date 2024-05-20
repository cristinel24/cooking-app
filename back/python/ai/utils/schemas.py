from typing import Optional

from pydantic import BaseModel


class ChatbotInput(BaseModel):
    user_id: str
    user_query: str


class TokenizeRecipeSchema(BaseModel):
    title: str
    prepTime: int
    tags: Optional[list[str]] = []
    allergens: Optional[list[str]] = []
    description: str
    ingredients: list[str]
    steps: list[str]


class ReplaceIngredientSchema(BaseModel):
    ingredient: str
    user_name: str
    recipe_name: str
    