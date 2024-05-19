from pydantic import BaseModel


class AllergensBody(BaseModel):
    allergens: list[str]
