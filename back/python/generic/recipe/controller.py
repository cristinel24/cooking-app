from fastapi import APIRouter, Path, Query

from recipe import schemas, services

router = APIRouter(
    prefix="/api"
)


@router.get("/get_recipe/{recipe_name}")
async def get_recipe(recipe_name: str):
    return {}


@router.post("/create_recipe")
async def create_recipe(data: schemas.RecipeData):
    return {}


@router.patch("/edit_recipe")
async def update_recipe(data: schemas.RecipeData):
    return {}


@router.delete("/delete_recipe/{name}")
async def delete_recipe(name: str):
    return {}


@router.get("/recipe_ratings/{parent_name}")
async def get_recipe_ratings(parent_name: str, start: int = Query(default=0), offset: int = Query(default=10)):
    ratings_data = schemas.GetRatingsData(parent_name=parent_name, start=start, offset=offset)
    ratings = services.get_recipe_ratings(ratings_data, offset-start)
    return ratings


@router.get("/rating_replies/{parent_name}")
async def get_rating_replies(data: schemas.GetRatingsData):
    return services.get_rating_replies(data, data.offset - data.start)


@router.post("/add_rating")
async def add_rating(data: schemas.RatingData):
    return services.add_rating(data)


@router.patch("/edit_rating/{parent_name}")
async def edit_rating(data: schemas.EditRatingData, parent_name: str = Path(...)):
    return services.edit_rating(data, parent_name)


@router.delete("/delete_rating/{rating_name}")
async def delete_rating(rating_name: str):
    return services.delete_rating(rating_name)
