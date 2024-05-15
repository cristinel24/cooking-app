from repository import *
import requests
from constants import *
from schemas import *
import exceptions

recipe_collection = RecipeCollection()


# commented code is for user card data

def get_recipe_by_id(recipe_id: str) -> RecipeData:
    recipe_data = recipe_collection.get_recipe_by_id(recipe_id)
    if not recipe_data:
        raise exceptions.RecipeException(ErrorCodes.NONEXISTENT_RECIPE.value)
    author_id = recipe_data.get("authorId")
    # user_card_data = get_user_card_data(author_id)
    # if not user_card_data:
    # return None
    recipe = {
        # "author": user_card_data,
        "title": recipe_data.get("title"),
        "description": recipe_data.get("description"),
        "prepTime": recipe_data.get("prepTime"),
        "steps": recipe_data.get("steps"),
        "ingredients": recipe_data.get("ingredients"),
        "allergens": recipe_data.get("allergens"),
        "tags": recipe_data.get("tags"),
        "thumbnail": recipe_data.get("thumbnail"),
        "viewCount": recipe_data.get("view_count")
    }
    return recipe


def get_user_card_data(user_id: str) -> UserCardData:
    url = f"{USER_MICROSERVICE_URL}/user/{user_id}/card"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise exceptions.RecipeException(ErrorCodes.SERVER_ERROR.value)


def get_recipe_card_by_id(recipe_id) -> RecipeCardData:
    recipe_data = recipe_collection.get_recipe_by_id(recipe_id)
    if not recipe_data:
        raise exceptions.RecipeException(ErrorCodes.NONEXISTENT_RECIPE.value)
    author_id = recipe_data.get("authorId")
    # user_card_data = get_user_card_data(author_id)
    # if not user_card_data:
    # return None
    recipe_card = {
        # "author": user_card_data,
        "title": recipe_data.get("title"),
        "description": recipe_data.get("description"),
        "prepTime": recipe_data.get("prepTime"),
        "tags": recipe_data.get("tags"),
        "allergens": recipe_data.get("allergens"),
        "thumbnail": recipe_data.get("thumbnail"),
        "viewCount": recipe_data.get("viewCount")
    }
    return recipe_card
