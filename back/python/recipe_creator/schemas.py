from pydantic import BaseModel


class RecipeData(BaseModel):
    title: str
    description: str
    prepTime: int
    steps: list[str]
    ingredients: list[str]
    allergens: list[str]
    tags: list[str]
    thumbnail: str
