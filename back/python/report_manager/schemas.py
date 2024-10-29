from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel

from rating_manager.schemas import RatingDataCard
from recipe_retriever.schemas import RecipeData
from user_retriever.schemas import UserCardData, UserData


class ReportCardData:
    id: str
    author: UserCardData
    reportedType: Literal["rating", "recipe", "user"]
    reportedEntity: RecipeData | UserData | RatingDataCard
    createdAt: datetime


class ReportsResponse(BaseModel):
    data: list[ReportCardData]
    total: int


class ReportCreateData(BaseModel):
    reportedType: str
    reportedId: str
    description: Optional[str]
    image: Optional[str]
