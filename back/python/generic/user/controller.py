from fastapi import APIRouter, HTTPException

from user.schemas import AccountChangeData
from user import services
from user.services import user_collection

router = APIRouter(
    prefix="/api/users"
)


@router.get("/{name}", tags=["users"])
async def get_user(name: str) -> dict:
    return await services.get_user(name)


@router.patch("/{name}", tags=["users"])
async def change_account_data(name: str, data: AccountChangeData) -> dict:
    return await services.change_account_data(name, data)


@router.put("/{name}/saved-recipes", tags=["users"])
async def save_recipe(name: str, recipe_name: str) -> dict:
    return await services.save_recipe(name, recipe_name)


@router.delete("/{name}/saved-recipes", tags=["users"])
async def unsave_recipe(name: str, recipe_name: str) -> dict:
    return await services.unsave_recipe(name, recipe_name)


@router.get("/{name}/saved-recipes", tags=["users"])
async def get_recipes(name: str) -> dict:
    return await services.get_recipes(name)


@router.put("/{name}/search-history", tags=["users"])
async def add_search(name: str, search: str) -> dict:
    return {"search": search}


@router.get("/{name}/search-history", tags=["users"])
async def get_search_history(name: str) -> dict:
    pass


@router.delete("/{name}/search-history", tags=["users"])
async def clear_search_history(name: str) -> dict:
    pass


@router.patch("/{name}/message-history", tags=["users"])
async def add_message(name: str, message: str) -> dict:
    return {"message": message}


@router.get("/{name}/message-history", tags=["users"])
async def get_message_history(name: str) -> dict:
    pass


@router.delete("/{name}/message-history", tags=["users"])
async def clear_message_history(name: str) -> dict:
    pass


@router.post("/{name}/following", tags=["users"])
async def add_follow(name: str, follow_name: str) -> dict:
    return await services.add_follow(name, follow_name)


@router.delete("/{name}/following", tags=["users"])
async def unfollow(name: str, follow_name: str) -> dict:
    return await services.unfollow(name, follow_name)


@router.get("/{name}/following", tags=["users"])
async def get_following(name: str, start: int, count: int) -> dict:
    return await services.get_following(name, start, count)


@router.get("/{name}/followers", tags=["users"])
async def get_followers(name: str) -> dict:
    pass
