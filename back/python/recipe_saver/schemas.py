from pydantic import BaseModel


class RecipeId(BaseModel):
    id: str
