from pydantic import BaseModel


class UserData(BaseModel):
    username: str | None = None
    displayName: str | None = None
    icon: str | None = None
    roles: int | None = None
    ratingAvg: float | None = None
    description: str | None = None
    recipes: list[str] | None = None
    ratings: list[str] | None = None


class UserCardData(BaseModel):
    username: str | None = None
    displayName: str | None = None
    icon: str | None = None
    roles: int | None = None
    ratingAvg: float | None = None


class UserFullData(BaseModel):
    username: str | None = None
    displayName: str | None = None
    icon: str | None = None
    roles: int | None = None
    ratingAvg: float | None = None
    description: str | None = None
    recipes: list[str] | None = None
    ratings: list[str] | None = None
    email: str | None = None
    followsCount: int | None = None
    followersCount: int | None = None
    allergens: list[str] | None = None
    searchHistory: list[str] | None = None
    messageHistory: list[str] | None = None
    savedRecipes: list[str] | None = None


class UserCardsRequestData(BaseModel):
    ids: list[str] | None = None


class ErrorCode(BaseModel):
    error_code: int
