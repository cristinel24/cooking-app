import json

from bson import json_util

from db.follow_collection import FollowCollection
from db.recipe_collection import RecipeCollection
from db.user_collection import UserCollection
from generic.user.schemas import AccountChangeData

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


async def get_user_profile(user_name: str) -> dict:
    user = user_collection.get_user_profile_by_name(user_name)
    user_rating = round(user["ratingSum"] / user["ratingCount"], 2) if user["ratingCount"] != 0 else 0
    del user["ratingSum"]
    del user["ratingCount"]
    user["rating"] = str(user_rating)

    return parse_json(user)


async def change_account_data(user_name: str, data: AccountChangeData) -> dict:
    updated_fields = dict()
    for item in data:
        if item[1] is not None:
            updated_fields[to_lower_camel_case(item[0])] = item[1]
    user_collection.update_user_by_name(user_name, updated_fields)
    return {"ok": 1}


async def save_recipe(user_name: str, recipe_name: str) -> dict:
    recipe_id = recipe_collection.find_recipe_id_by_name(recipe_name)
    user = user_collection.get_user_by_name(user_name)
    if recipe_id not in user["savedRecipes"]:
        user_collection.update_saved_recipes_by_name(user_name, recipe_id)
    return {"recipe": recipe_name}


async def unsave_recipe(user_name: str, recipe_name: str) -> dict:
    recipe_id = recipe_collection.find_recipe_id_by_name(recipe_name)
    user_collection.delete_saved_recipe_by_name(user_name, recipe_id)
    return {"ok": 1}


async def get_recipes(user_name: str) -> dict:
    user = user_collection.get_user_by_name(user_name)
    saved_recipes_list = list()
    for saved_recipe_id in user["savedRecipes"]:
        recipe = recipe_collection.find_recipe_card_by_id(saved_recipe_id)
        recipe["author"] = user_collection.get_user_name_by_id(recipe["authorId"])
        del recipe["authorId"]
        saved_recipes_list.append(recipe)
    response = {
        "name": user["name"],
        "savedRecipes": saved_recipes_list
    }
    return parse_json(response)


async def add_search(user_name: str, search: str) -> dict:
    user_collection.update_search_by_name(user_name, search)
    return {"ok": 1}


async def clear_search_history(user_name: str) -> dict:
    user_collection.delete_search_history_by_name(user_name)
    return {"ok": 1}


async def get_search_history(user_name: str) -> dict:
    user = user_collection.get_user_by_name(user_name)
    search_history = user_collection.get_search_history_by_name(user_name)
    response = {"searchHistory": search_history}
    return parse_json(response)


async def add_message(user_name: str, message: str) -> dict:
    user_collection.update_message_by_name(user_name, message)
    return {"ok": 1}


async def clear_message_history(user_name: str) -> dict:
    user_collection.delete_message_history_by_name(user_name)
    return {"ok": 1}


async def get_message_history(user_name: str) -> dict:
    message_history = user_collection.get_message_history_by_name(user_name)
    response = {"messageHistory": message_history}
    return parse_json(response)


async def add_follow(user_name: str, followee_name: str) -> dict:
    user_id = user_collection.get_user_id_by_name(user_name)
    followee_id = user_collection.get_user_id_by_name(followee_name)
    if follow_collection.get_follow(user_id, followee_id) is None:
        follow_collection.insert_follow(user_id, followee_id)
    return {"ok": 1}


async def unfollow(user_name: str, follow_name: str) -> dict:
    user_id = user_collection.get_user_id_by_name(user_name)
    followee_id = user_collection.get_user_id_by_name(follow_name)
    follow_collection.delete_follow(user_id, followee_id)
    return {"ok": 1}


async def get_following(user_name: str, start: int, count: int) -> dict:
    user_id = user_collection.get_user_id_by_name(user_name)
    following_ids = follow_collection.get_following_by_user_id(user_id, start, count)
    following = list()
    for following_id in following_ids:
        following.append(user_collection.get_user_name_by_id(following_id))
    response = {"following": following}
    return parse_json(response)


async def get_followers(user_name: str, start: int, count: int) -> dict:
    user_id = user_collection.get_user_id_by_name(user_name)
    follower_ids = follow_collection.get_followers_by_user_id(user_id, start, count)
    followers = list()
    for follower_id in follower_ids:
        followers.append(user_collection.get_user_name_by_id(follower_id))
    response = {"followers": followers}
    return parse_json(response)
