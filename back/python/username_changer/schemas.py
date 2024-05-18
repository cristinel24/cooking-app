from typing import Annotated
from pydantic import BaseModel, Field


class UsernameChange(BaseModel):
    username: Annotated[str, Field(min_length=8, max_length=64, pattern=r'^[A-Za-z0-9_\\.]+$')]
    token: str
