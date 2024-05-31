from typing import Annotated

import uvicorn
from fastapi import FastAPI, Header, status
from fastapi.responses import JSONResponse

import services
from constants import *
from exception import RecipeDestroyerException

load_dotenv()

app = FastAPI(title="Recipe Destroyer")


@app.delete(
    path="/{recipe_id}",
    tags=["recipe-destroyer"],
    response_model=None,
    response_description="Successful operation"
)
async def delete_recipe(
        recipe_id: str,
        x_user_id: Annotated[str | None, Header()] = None,
        x_user_roles: Annotated[str | None, Header()] = None
) -> None | JSONResponse:
    if x_user_id is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"errorCode": ErrorCodes.UNAUTHENTICATED.value}
        )

    try:
        user_roles = int(x_user_roles)
    except ValueError:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"errorCode": ErrorCodes.USER_ROLES_INVALID_VALUE.value})

    try:
        await services.delete(recipe_id, x_user_id, user_roles)
    except RecipeDestroyerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
