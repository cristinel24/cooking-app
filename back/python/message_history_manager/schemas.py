from pydantic import BaseModel


class Message(BaseModel):
    message: str


class History(BaseModel):
    history: list[str]
