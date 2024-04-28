from fastapi import APIRouter

from generic.user import services
from generic.user.schemas import AccountChangeData

router = APIRouter(
    prefix="/api/users"
)


@router.get("/{user_name}", tags=["users"])
async def get_user_profile(user_name: str) -> dict:
    return await services.get_user_profile(user_name)


@router.patch("/{user_name}", tags=["users"])
async def change_account_data(user_name: str, data: AccountChangeData) -> dict:
    return await services.change_account_data(user_name, data)


@router.post("/{user_name}/saved-recipes", tags=["users"])
async def save_recipe(user_name: str, recipe_name: str) -> dict:
    return await services.save_recipe(user_name, recipe_name)


@router.delete("/{user_name}/saved-recipes", tags=["users"])
async def unsave_recipe(user_name: str, recipe_name: str) -> dict:
    return await services.unsave_recipe(user_name, recipe_name)


@router.get("/{user_name}/saved-recipes", tags=["users"])
async def get_recipes(user_name: str) -> dict:
    return await services.get_recipes(user_name)


@router.post("/{user_name}/search-history", tags=["users"])
async def add_search(user_name: str, search: str) -> dict:
    return await services.add_search(user_name, search)


@router.delete("/{user_name}/search-history", tags=["users"])
async def clear_search_history(user_name: str) -> dict:
    return await services.clear_search_history(user_name)


@router.get("/{user_name}/search-history", tags=["users"])
async def get_search_history(user_name: str) -> dict:
    return await services.get_search_history(user_name)


@router.post("/{user_name}/message-history", tags=["users"])
async def add_message(user_name: str, message: str) -> dict:
    return await services.add_message(user_name, message)


@router.delete("/{user_name}/message-history", tags=["users"])
async def clear_message_history(user_name: str) -> dict:
    return await services.clear_message_history(user_name)


@router.get("/{user_name}/message-history", tags=["users"])
async def get_message_history(user_name: str) -> dict:
    return await services.get_message_history(user_name)


@router.put("/{user_name}/following", tags=["users"])
async def add_follow(user_name: str, follow_name: str) -> dict:
    return await services.add_follow(user_name, follow_name)


@router.delete("/{user_name}/following", tags=["users"])
async def unfollow(user_name: str, follow_name: str) -> dict:
    return await services.unfollow(user_name, follow_name)


@router.get("/{user_name}/following", tags=["users"])
async def get_following(user_name: str, start: int, count: int) -> dict:
    return await services.get_following(user_name, start, count)


@router.get("/{user_name}/followers", tags=["users"])
async def get_followers(user_name: str, start: int, count: int) -> dict:
    return await services.get_followers(user_name, start, count)
