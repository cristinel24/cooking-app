from pydantic import json

from recipe import schemas
from db import recipe_collection
from db import user_collection


def get_recipe(recipe_name: str) -> dict:
    recipe_data = recipe_collection.get_recipe_by_name(recipe_name)
    if recipe_data:
        return json.loads(recipe_data)
    else:
        return {}


def add_tokens(recipe_name: str):
    pass


def create_recipe(data: schemas.RecipeData) -> dict:
    inserted_id = recipe_collection.insert_recipe(data.dict())
    return {"id": str(inserted_id)}


def update_recipe(data: schemas.RecipeData):
    pass


def delete_recipe(name: str):
    pass


def get_recipe_ratings(data: schemas.GetRatingsData):
    pass


def get_rating_replies(data: schemas.GetRatingsData):
    pass


def add_rating(data: schemas.RatingData) -> dict:
    inserted_id = recipe_collection.insert_rating(data.dict())
    return {"id": str(inserted_id)}


def edit_rating(data: schemas.EditRatingData):
    existing_rating = recipe_collection.get_rating_by_name(data.rating_name)
    if existing_rating:
        updated_count = recipe_collection.update_rating(existing_rating["_id"], data.dict())
        return {"updated_count": updated_count}
    else:
        return {"error": "Rating not found with the provided name"}


def delete_rating(rating_name: str):
    existing_rating = recipe_collection.get_rating_by_name(rating_name)

    if existing_rating:
        deleted_count = recipe_collection.delete_rating(existing_rating["_id"])
        return {"deleted_count": deleted_count}
    else:
        return {"error": "Rating not found with the provided name"}
