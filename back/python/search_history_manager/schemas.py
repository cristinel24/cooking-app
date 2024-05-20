from pydantic import BaseModel

class Search(BaseModel):
    search: str

class History(BaseModel):
    history: list[str]
