from pydantic import BaseModel


class UserCardData(BaseModel):
    id: str
    username: str
    displayName: str
    icon: str
    roles: int
    ratingAvg: float


class RecipeData(BaseModel):
    id: str
    author: UserCardData
    title: str
    description: str
    prepTime: int
    steps: list[str]
    ingredients: list[str]
    allergens: list[str]
    tags: list[str]
    thumbnail: str
    viewCount: int


class RecipeCardData(BaseModel):
    id: str
    author: UserCardData
    title: str
    description: str
    prepTime: int
    tags: list[str]
    allergens: list[str]
    thumbnail: str
    viewCount: int
