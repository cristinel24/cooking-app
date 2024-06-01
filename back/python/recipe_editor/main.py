from typing import Annotated

from fastapi import FastAPI, status
from fastapi.params import Header
from fastapi.responses import JSONResponse

import services
from constants import HOST, PORT, ErrorCodes
from exception import RecipeEditorException
from schemas import RecipeData

app = FastAPI(title="Recipe Editor")


@app.patch("/{recipe_id}", response_model=None, response_description="Successful operation")
async def edit_recipe(
        recipe_id: str, recipe_data: RecipeData,
        x_user_id: Annotated[str | None, Header()] = None,
        x_user_roles: Annotated[str | None, Header()] = None
) -> None | JSONResponse:
    if not x_user_id or not x_user_roles:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"errorCode": ErrorCodes.NOT_AUTHENTICATED.value})

    try:
        user_roles = int(x_user_roles)
    except ValueError:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"errorCode": ErrorCodes.USER_ROLES_INVALID_VALUE.value})

    try:
        await services.edit_recipe(x_user_id, user_roles, recipe_id, recipe_data)
    except RecipeEditorException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
