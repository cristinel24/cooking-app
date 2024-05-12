from repository import *

user_collection = UserCollection()


def save_recipe(user_id: str, recipe_id: str):
    user_collection.add_recipe_to_user(user_id, recipe_id)


def remove_recipe_from_saved(user_id: str, recipe_id: str):
    user_collection.remove_recipe_from_saved(user_id, recipe_id)
