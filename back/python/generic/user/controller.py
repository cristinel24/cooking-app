from user import schemas

from fastapi import APIRouter

router = APIRouter(
    prefix="/api"
)


@router.get("/users/{name}", tags=["users"])
async def get_user(name: str) -> dict:
    return {"name": name}


# session token needed
@router.patch("/users/{name}", tags=["users"])
async def change_account_data(name: str, data: schemas.AccountChangeData) -> dict:
    return {"name": name, "data": data.dict()}


# admin action
@router.delete("/users/{name}", tags=["admin"])
async def delete_user(name: str) -> dict:
    return {"name": name}


# admin action
# todo determine how the role is passed to us
@router.patch("/admin/{solver_name}/users/{name}", tags=["admin"])
async def change_user_role(solver_name: str, name: str, role: int) -> dict:
    return {"name": name, "role": role}


# session token needed for the rest of the functions
@router.patch("/users/{name}/saved-recipes/{recipe_name}", tags=["users"])
async def save_recipe(name: str, recipe_name: str) -> dict:
    return {"name": name, "recipe_name": recipe_name}

