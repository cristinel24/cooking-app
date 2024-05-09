from fastapi import APIRouter
from generic.recipe import schemas, services

router = APIRouter(
    prefix="/api/recipe"
)


@router.get("/{recipe_name}", tags=["recipe"])
async def get_recipe(recipe_name: str):
    return services.get_recipe(recipe_name)


@router.get("/{recipe_name}/card", tags=["recipe"])
async def get_recipe_card(recipe_name: str):
    return services.get_recipe_card(recipe_name)


@router.put("/", tags=["recipe"])
async def create_recipe(data: dict):
    return services.create_recipe(data)


@router.patch("/{recipe_name}", tags=["recipe"])
async def update_recipe(data: schemas.RecipeData):
    services.update_recipe(dict(data))


@router.delete("/{recipe_name}", tags=["recipe"])
async def delete_recipe(recipe_name: str):
    services.delete_recipe(recipe_name)


@router.get("/{recipe_name}/ratings", tags=["recipe"])
async def get_recipe_ratings(recipe_name: str, start: int, offset: int):
    return services.get_recipe_ratings(schemas.GetRatingsData(parent_name=recipe_name, start=start, offset=offset))


@router.get("/{rating_name}/replies", tags=["recipe"])
async def get_rating_replies(rating_name: str, start: int, offset: int):
    return services.get_rating_replies(schemas.GetRatingsData(parent_name=rating_name, start=start, offset=offset))


# TODO: find a better solution
@router.post("/add_rating", tags=["recipe"])
async def add_rating(data: schemas.RatingData):
    services.add_rating(data)


@router.patch("/edit_rating/{parent_name}", tags=["recipe"])
async def edit_rating(data: schemas.EditRatingData, parent_name: str):
    services.edit_rating(data, parent_name)


@router.delete("/delete_rating/{rating_name}", tags=["recipe"])
async def delete_rating(rating_name: str):
    # TODO: delete doesn't work as specified yet
    services.delete_rating(rating_name)
