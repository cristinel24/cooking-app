from pydantic import BaseModel


class TagsBody(BaseModel):
    tags: list[str]
