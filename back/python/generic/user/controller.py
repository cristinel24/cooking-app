import schemas

from fastapi import APIRouter

from ..main import router


@router.get("{name}")
async def get_user(name: str) -> dict:
    return {"name": name}


# session token needed
@router.patch("{name}/change-data")
async def change_account_data(name: str, data: schemas.AccountChangeData) -> dict:
    return {"name": name, "data": data.dict()}


# admin action
@router.delete("{name}/delete-user")
async def delete_user(name: str) -> dict:
    return {"name": name}


# admin action
# todo determine how the role is passed to us
@router.patch("{name}/change-role")
async def change_user_role(solver_name: str, name: str, role: int) -> dict:
    return {"name": name, "role": role}


# session token needed for the rest of the functions
@router.patch("{name}/{recipe_name}")
async def save_recipe(name: str, recipe_name: str) -> dict:
    return {"name": name, "recipe_name": recipe_name}
