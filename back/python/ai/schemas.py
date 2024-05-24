from pydantic import BaseModel


class ChatbotInput(BaseModel):
    userQuery: str


class RecipeData(BaseModel):
    title: str
    prepTime: int
    tags: list[str]
    allergens: list[str]
    description: str
    ingredients: list[str]
    steps: list[str]


class ReplaceIngredientData(BaseModel):
    ingredient: str
    userId: str
    recipeId: str


class ReplaceIngredientsList(BaseModel):
    replaceOptions: list[str]


class GeneratedTokens(BaseModel):
    tokens: list[str]


class ChatbotResponse(BaseModel):
    response: str
    