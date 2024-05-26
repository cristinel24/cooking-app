from typing import Annotated
from fastapi.responses import JSONResponse
import uvicorn
from fastapi import Header, status, FastAPI

import services, constants, exceptions

app = FastAPI(title="Recipe Saver")


@app.put("/{user_id}/saved-recipes/{recipe_id}", tags=["user-actions"], response_model=None, response_description="Successful operation")
async def save_recipe(user_id: str, recipe_id: str, x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    if x_user_id != user_id:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errorCode": constants.ErrorCodes.WRONG_USER_ID.value})

    try:
        services.save_recipe(user_id, recipe_id)
    except (exceptions.RecipeSaverException,) as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,) as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": constants.ErrorCodes.SERVER_ERROR.value})


@app.delete("/{user_id}/saved-recipes/{recipe_id}", tags=["user-actions"], response_model=None, response_description="Successful operation")
async def remove_recipe_from_saved(user_id: str, recipe_id: str, x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    if x_user_id != user_id:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errorCode": constants.ErrorCodes.WRONG_USER_ID.value})

    try:
        services.remove_recipe_from_saved(user_id, recipe_id)
    except (exceptions.RecipeSaverException,) as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,) as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": constants.ErrorCodes.SERVER_ERROR.value})


if __name__ == "__main__":
    uvicorn.run(app, host=constants.HOST, port=constants.PORT)
