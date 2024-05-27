from pydantic import BaseModel, Field

class AuthorCardData(BaseModel):
    id: str
    username: str
    displayName: str
    icon: str
    roles: int
    ratingAvg: float
class RatingDataCard(BaseModel):
    parentId: str
    parentType: str
    author: AuthorCardData
    rating: int = Field(0, ge=0, le=5, description="An integer value between 0 and 5")
    description: str


class RatingListResponse(BaseModel):
    ratings: list[RatingDataCard]
    total: int

class RatingCreateRequest(BaseModel):
    authorId: str
    description: str
    rating: int = Field(..., ge=1, le=5, description="Rating value between 1 and 5")
    parentType: str = "recipe"

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
