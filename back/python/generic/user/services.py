from user import schemas
from user.collection import UserCollection, RecipeCollection, FollowCollection

user_collection = UserCollection()
recipe_collection = RecipeCollection()
follow_collection = FollowCollection()


async def get_user(name: str) -> dict:
    return user_collection.get_user_by_name(name)


async def change_account_data(name: str, data: schemas.AccountChangeData) -> dict:
    return {"name": name, "data": data.dict()}


async def add_recipe(name: str, recipe_name: str) -> dict:
    return {"name": name, "recipe_name": recipe_name}


async def get_recipes(name: str) -> dict:
    pass


async def delete_recipe(name: str, recipe_name: str) -> dict:
    pass


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
    pass


async def get_following(name: str, start: int, count: int) -> dict:
    pass


async def unfollow(name: str, follow_name: str) -> dict:
    pass


async def get_followers(name: str) -> dict:
    pass
