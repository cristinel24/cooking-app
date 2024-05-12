from repository import *
from constants import ErrorCodes
import exceptions

recipe_collection = RecipeCollection()
user_collection = UserCollection()


def save_recipe(user_id : str, recipe_id : str):
    user = user_collection.get_user_by_id(user_id)
    if user is None:
        raise exceptions.RecipeSaverException(ErrorCodes.NONEXISTENT_USER.value)
    recipe = recipe_collection.get_recipe_by_id(recipe_id)
    if recipe is None:
        raise exceptions.RecipeSaverException(ErrorCodes.NONEXISTENT_RECIPE.value)
    if recipe_id in user["savedRecipes"]:
        raise exceptions.RecipeSaverException(ErrorCodes.RECIPE_ALREADY_SAVED.value)
    user_collection.add_recipe_to_user(user_id, recipe_id)


def remove_recipe_from_saved(user_id : ObjectId, recipe_id : ObjectId):
    user = user_collection.get_user_by_id(user_id)
    if user is None:
        raise exceptions.RecipeSaverException(ErrorCodes.NONEXISTENT_USER.value)
    recipe = recipe_collection.get_recipe_by_id(recipe_id)
    if recipe is None:
        raise exceptions.RecipeSaverException(ErrorCodes.NONEXISTENT_RECIPE.value)
    if recipe_id not in user["savedRecipes"]:
        raise exceptions.RecipeSaverException(ErrorCodes.RECIPE_NOT_SAVED.value)
    user_collection.remove_recipe_from_user(user_id, recipe_id)