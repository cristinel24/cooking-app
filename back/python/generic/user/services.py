import json
from pprint import pprint

from user.schemas import AccountChangeData
from user.collection import UserCollection, RecipeCollection, FollowCollection
from bson import json_util

user_collection = UserCollection()
recipe_collection = RecipeCollection()
follow_collection = FollowCollection()


def parse_json(data):
    return json.loads(json_util.dumps(data))


def to_camel_case(snake_str: str) -> str:
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def to_lower_camel_case(snake_str: str) -> str:
    camel_string = to_camel_case(snake_str)
    return snake_str[0].lower() + camel_string[1:]


async def get_user(user_name: str) -> dict:
    return user_collection.get_user_by_name(user_name)


async def change_account_data(user_name: str, data: AccountChangeData) -> dict:
    updated_fields = dict()
    for item in data:
        if item[1] is not None:
            updated_fields[to_lower_camel_case(item[0])] = item[1]
    pprint(updated_fields)
    user_collection.update_user_by_name(user_name, updated_fields)
    return {"name": user_name, "data": data.dict()}


# to be tested
async def save_recipe(user_name: str, recipe_name: str) -> dict:
    recipe_id = recipe_collection.find_recipe_by_name(recipe_name)["_id"]
    user_collection.update_saved_recipes_by_name(user_name, recipe_id)
    return {"name": user_name, "recipe": recipe_name}


# for now retrieves all info about the recipe
# it should retrieve only what a recipe card contains
async def get_recipes(user_name: str) -> dict:
    user = user_collection.get_user_by_name(user_name)
    saved_recipes_list = list()
    for saved_recipe_id in user["savedRecipes"]:
        recipe = recipe_collection.find_recipe_by_id(saved_recipe_id)
        del recipe["_id"]
        pprint(recipe)
        saved_recipes_list.append(recipe)
    response = {
        "name": user["name"],
        "savedRecipes": saved_recipes_list
    }
    return parse_json(response)


async def unsave_recipe(name: str, recipe_name: str) -> dict:
    return user_collection.unsave_recipe(name, recipe_name)


async def add_search(name: str, search: str) -> dict:
    return {"search": search}


async def get_search_history(name: str) -> dict:
    pass


async def clear_search_history(name: str) -> dict:
    pass


async def add_message(name: str, message: str) -> dict:
    return {"message": message}


async def get_message_history(name: str) -> dict:
    pass


async def clear_message_history(name: str) -> dict:
    pass


async def add_follow(name: str, follow_name: str) -> dict:
    return user_collection.add_follow(name, follow_name)


async def get_following(name: str, start: int, count: int) -> dict:
    return user_collection.get_following(name, start, count)


async def unfollow(name: str, follow_name: str) -> dict:
    return user_collection.delete_follow(name, follow_name)


async def get_followers(name: str, start: int, count: int) -> dict:
    return user_collection.get_followers(name, start, count)
