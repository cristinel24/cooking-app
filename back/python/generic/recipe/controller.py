from fastapi import APIRouter

from recipe import schemas

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
async def get_recipe_ratings(data: schemas.GetRatingsData):
    return {}


@router.get("/rating_replies/{parent_name}")
async def get_rating_replies(data: schemas.GetRatingsData):
    return {}


@router.post("/add_rating")
async def add_rating(data: schemas.RatingData):
    return {}


@router.patch("/edit_rating/{rating_name}")
async def edit_rating(data: schemas.EditRatingData):
    return {}


@router.delete("/delete_rating/{rating_name}")
async def delete_rating(rating_name: str):
    return {}