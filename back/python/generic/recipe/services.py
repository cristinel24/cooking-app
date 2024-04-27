import json
from bson import json_util
from typing import List

from db import recipe_collection
from recipe import schemas

from db.recipe_collection import RecipeCollection

recipe = RecipeCollection()

def get_recipe(recipe_name: str) -> dict:
    try:
        recipe_data = recipe.get_recipe_by_name(recipe_name)
        return recipe_data
    except Exception as e:
        raise Exception(f"Failed to get recipe by name! - {str(e)}")


def add_tokens(recipe_name: str, recipe_tokens: list[str]):
    try:
        recipe_data = RecipeCollection.add_tokens_by_name(recipe_name, recipe_tokens)
        return json.loads(recipe_data) if recipe_data else {}
    except Exception as e:
        raise Exception(f"Failed to add tokens to recipe! - {str(e)}")


def create_recipe(data) -> dict:
    try:
        inserted_id = recipe.insert_recipe(data)
        return {"id": str(inserted_id)}
    except Exception as e:
        raise Exception(f"Failed to create recipe! - {str(e)}")


def update_recipe(recipe_id: str, update_data: dict):
    try:
        print(update_data)
        recipe_data = recipe.update_recipe_by_id(recipe_id, update_data)
        return json.loads(json_util.dumps(recipe_data))
    except Exception as e:
        raise Exception(f"Failed to update recipe! - {str(e)}")


def delete_recipe(recipe_id: str):
    try:
        recipe_data = recipe.delete_recipe_by_id(recipe_id)
        return recipe_data
    except Exception as e:
        raise Exception(f"Failed to delete recipe! - {str(e)}")

