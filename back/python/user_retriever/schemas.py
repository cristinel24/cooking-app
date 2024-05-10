from pydantic import BaseModel


class UserData(BaseModel):
    username: str | None = None
    displayName: str | None = None
    icon: str | None = None
    roles: int | None = None
    ratingAvg: int | None = None
    description: str | None = None
    recipes: list[str] | None = None
    ratings: list[str] | None = None


class UserCardData(BaseModel):
    username: str | None = None
    displayName: str | None = None
    icon: str | None = None
    roles: int | None = None
    ratingAvg: int | None = None


class UserFullData(BaseModel):
    username: str | None = None
    displayName: str | None = None
    icon: str | None = None
    roles: int | None = None
    ratingAvg: int | None = None
    description: str | None = None
    recipes: list[str] | None = None
    ratings: list[str] | None = None
    email: str | None = None
    messageHistory: list[str] | None = None
    searchHistory: list[str] | None = None
    allergens: list[str] | None = None
    savedRecipes: list[str] | None = None
    ratingAvg: int | None = None
    followers: list[str] | None = None
    follows: list[str] | None = None
