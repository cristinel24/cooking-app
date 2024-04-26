from pydantic import json

from recipe import schemas
from db import recipe_collection
from db import user_collection


def get_recipe(recipe_name: str) -> dict:
    recipe_data = recipe_collection.get_recipe_by_name(recipe_name)
    return json.loads(recipe_data) if recipe_data else {}


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
    inserted_id = recipe_collection.add_rating(data.dict())
    return {"id": str(inserted_id)}


def edit_rating(data: schemas.EditRatingData):
    pass


def delete_rating(rating_name: str):
    pass
