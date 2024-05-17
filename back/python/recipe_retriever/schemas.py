from pydantic import BaseModel


class UserCardData(BaseModel):
    username: str
    displayName: str
    icon: str
    roles: list[str]
    ratingAvg: float


class RecipeData(BaseModel):
    title: str
    description: str
    prepTime: str
    steps: list[str]
    ingredients: list[str]
    allergens: list[str]
    tags: list[str]
    thumbnail: str
    viewCount: int


class RecipeCardData(BaseModel):
    title: str
    description: str
    prepTime: str
    tags: list[str]
    allergens: list[str]
    thumbnail: str
    viewCount: int
