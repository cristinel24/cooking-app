import os
import sys
import json
from bson import json_util

###pentru import de module(nu)
sys.path.insert(1, os.path.join(sys.path[0], '..'))
sys.path.insert(2, os.path.join(sys.path[0], '../..'))

from db import recipe_collection

recipe_operation = recipe_collection.RecipeCollection()


def get_recipe(recipe_name: str) -> dict:
    return recipe_operation.get_recipe_by_name(recipe_name)


def get_recipe_card(recipe_name: str) -> dict:
    return recipe_operation.get_recipe_card(recipe_name)


def add_tokens(recipe_name: str, recipe_tokens: list[str]) -> None:
    recipe_operation.add_tokens_by_name(recipe_name, recipe_tokens)


def create_recipe(data) -> None:
    recipe_operation.insert_recipe(data)


def update_recipe(data: dict) -> None:
    recipe_operation.update_recipe_by_name(data)


def delete_recipe(name: str):
    return recipe_operation.delete_recipe_by_name(name)
