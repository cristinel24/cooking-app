from typing import List, Tuple
from pydantic import BaseModel


class UserProfileData(BaseModel):
    icon: str | None = None
    displayName: str | None = None
    description: str | None = None
    allergens: List[Tuple[int, str]] | None = None
