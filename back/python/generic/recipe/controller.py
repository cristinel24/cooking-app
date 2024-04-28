from fastapi import APIRouter

from recipe import schemas, services

router = APIRouter(
    prefix="/api"
)


@router.get("/recipe_ratings/{parent_name}")
async def get_recipe_ratings(parent_name: str, start: int, offset: int):
    return services.get_recipe_ratings(schemas.GetRatingsData(parent_name=parent_name, start=start, offset=offset))


@router.get("/rating_replies/{parent_name}")
async def get_rating_replies(parent_name: str, start: int, offset: int):
    return services.get_rating_replies(schemas.GetRatingsData(parent_name=parent_name, start=start, offset=offset))


@router.post("/add_rating")
async def add_rating(data: schemas.RatingData):
    services.add_rating(data)


@router.patch("/edit_rating/{parent_name}")
async def edit_rating(data: schemas.EditRatingData, parent_name: str):
    services.edit_rating(data, parent_name)


@router.delete("/delete_rating/{rating_name}")
async def delete_rating(rating_name: str):
    services.delete_rating(rating_name)
