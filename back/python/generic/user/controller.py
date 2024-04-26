from user import schemas

from fastapi import APIRouter

router = APIRouter(
    prefix="/api/users"
)


@router.get("/{name}", tags=["users"])
async def get_user(name: str) -> dict:
    return {"name": name}


@router.patch("/{name}", tags=["users"])
async def change_account_data(name: str, data: schemas.AccountChangeData) -> dict:
    return {"name": name, "data": data.dict()}


@router.put("/{name}/saved-recipes", tags=["users"])
async def add_recipe(name: str, recipe_name: str) -> dict:
    return {"name": name, "recipe_name": recipe_name}


@router.get("/{name}/saved-recipes", tags=["users"])
async def get_recipes(name: str) -> dict:
    pass


@router.delete("/{name}/saved-recipes", tags=["users"])
async def delete_recipe(name: str, recipe_name: str) -> dict:
    pass


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
    pass


@router.get("/{name}/following", tags=["users"])
async def get_following(name: str, start: int, count: int) -> dict:
    pass


@router.delete("/{name}/following", tags=["users"])
async def unfollow(name: str, follow_name: str) -> dict:
    pass


@router.get("/{name}/followers", tags=["users"])
async def get_followers(name: str) -> dict:
    pass
