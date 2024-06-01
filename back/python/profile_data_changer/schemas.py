from typing import List, Tuple
from pydantic import BaseModel
from repository import UserCollection

user_collection = UserCollection()


class UserProfileData(BaseModel):
    icon: str | None = None
    displayName: str | None = None
    description: str | None = None
    allergens: List[str] | None = None
