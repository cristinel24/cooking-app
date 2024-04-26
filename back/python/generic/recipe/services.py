
import os
import sys
import json
from bson import json_util

###pentru import de module(nu)
sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.insert(2, os.path.join(sys.path[0], '../..'))

from recipe import schemas

from db.recipe_collection import RecipeCollection

x=RecipeCollection()

def get_recipe(recipe_name: str) -> dict:
    recipe_data = x.get_recipe_by_name(recipe_name)
    return recipe_data


def add_tokens(recipe_name: str, recipe_tokens:list[str]):
    recipe_data= RecipeCollection.add_tokens_by_name(recipe_name,recipe_tokens)
    return json.loads(recipe_data) if recipe_data else {}


def create_recipe(data) -> dict:
    inserted_id = x.insert_recipe(data)
    return {"id": str(inserted_id)}


def update_recipe(recipe_name: str, update_data: dict):
    print(update_data)
    recipe_data = x.update_recipe_by_name(recipe_name,update_data)
    return json.loads(json_util.dumps(recipe_data))


def delete_recipe(name: str):
    recipe_data=x.delete_recipe_by_name(name)
    return recipe_data


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
