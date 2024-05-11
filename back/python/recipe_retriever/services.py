from typing import Any

from repository import *
import requests
from constants import USER_MICROSERVICE_URL

recipe_collection = RecipeCollection()


def get_recipe_by_id(recipe_id: ObjectId) -> Any | None:
    recipe_data = recipe_collection.get_recipe_by_id(recipe_id)

    if not recipe_data:
        return None

    author_id = recipe_data.get("authorId")

    if not author_id:
        return None

    #user_card_data = get_user_card_data(author_id)

    #if not user_card_data:
        #return None

    recipe = {
        #"author": user_card_data,
        "title": recipe_data.get("title"),
        "description": recipe_data.get("description"),
        "prepTime": recipe_data.get("prepTime"),
        "steps": recipe_data.get("steps"),
        "ingredients": recipe_data.get("ingredients"),
        "allergens": recipe_data.get("allergens"),
        "tags": recipe_data.get("tags"),
        "thumbnail": recipe_data.get("thumbnail"),
        # "viewCount": view_count
    }

    return recipe


def get_user_card_data(user_id: ObjectId) -> Any | None:
    url = f"{USER_MICROSERVICE_URL}/user/{user_id}/card"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Unable to fetch user card data. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error: Unable to connect to user microservice. {e}")
        return None


def get_recipe_card_by_id(recipe_id):
    recipe_data = recipe_collection.get_recipe_by_id(recipe_id)

    if not recipe_data:
        return None

    author_id = recipe_data.get("authorId")

    if not author_id:
        return None

    #user_card_data = get_user_card_data(author_id)

    #if not user_card_data:
        #return None

    recipe_card = {
        #"author": user_card_data,
        "title": recipe_data.get("title"),
        "description": recipe_data.get("description"),
        "prepTime": recipe_data.get("prepTime"),
        "tags": recipe_data.get("tags"),
        "allergens": recipe_data.get("allergens"),
        "thumbnail": recipe_data.get("thumbnail"),
        #"viewCount": recipe_data.get("viewCount")
    }

    return recipe_card
