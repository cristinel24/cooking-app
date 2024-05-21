from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

class Rating(BaseModel):
    id: str
    authorId: str
    description: str
    rating: int
    createdAt: datetime
    updatedAt: datetime

class RatingCreateRequest(BaseModel):
    authorId: str
    description: str
    rating: int = Field(..., ge=1, le=5, description="Rating value between 1 and 5")

class RatingListResponse(BaseModel):
    ratings: List[Rating]
    total: int

class RatingCreateResponse(BaseModel):
    message: str = "Rating created successfully"

class RatingUpdateRequest(BaseModel):
    description: str
    rating: int = Field(..., ge=0, le=5, description="Rating value between 0 and 5")

class RatingUpdateResponse(BaseModel):
    message: str = "Rating updated successfully"


# Schemas for DELETE /recipe/{recipe_id}/ratings/{rating_id}
class RatingDeleteResponse(BaseModel):
    message: str = "Rating deleted successfully"


USER_PROJECTION = {
    "id": 1,
    "ratingSum": 1,
    "ratingCount": 1
}

RECIPE_PROJECTION = {
    "id": 1,
    "ratingSum": 1,
    "ratingCount": 1
}
