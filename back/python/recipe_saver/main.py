from typing import Annotated

import uvicorn
from fastapi import Header, status, FastAPI
from fastapi.responses import JSONResponse

import constants
import exceptions
import services
from schemas import SavedRecipesModel

app = FastAPI(title="Recipe Saver")


@app.put("/{user_id}/saved-recipes/{recipe_id}", tags=["user-actions"], response_model=None,
         response_description="Successful operation")
async def save_recipe(user_id: str, recipe_id: str,
                      x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    if not x_user_id:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"errorCode": constants.ErrorCodes.UNAUTHORIZED_REQUEST.value})
    if x_user_id != user_id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content={"errorCode": constants.ErrorCodes.FORBIDDEN_REQUEST.value})

    try:
        services.save_recipe(user_id, recipe_id)
    except (exceptions.RecipeSaverException,) as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,) as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": constants.ErrorCodes.SERVER_ERROR.value})


@app.get("/{user_id}/saved-recipes/", tags=["user-actions"], response_model=SavedRecipesModel)
async def get_saved_recipes(user_id: str, start: int, count: int,
                            x_user_id: Annotated[str | None, Header()] = None) -> SavedRecipesModel | JSONResponse:
    if not x_user_id:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"errorCode": constants.ErrorCodes.UNAUTHORIZED_REQUEST.value})

    if x_user_id != user_id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content={"errorCode": constants.ErrorCodes.FORBIDDEN_REQUEST.value})

    try:
        total, data = await services.get_recipes(user_id, start, count)
        return SavedRecipesModel(total=total, data=data)
    except exceptions.RecipeSaverException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,) as e:
        print(e)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": constants.ErrorCodes.SERVER_ERROR.value})


@app.delete("/{user_id}/saved-recipes/{recipe_id}", tags=["user-actions"], response_model=None,
            response_description="Successful operation")
async def remove_recipe_from_saved(user_id: str, recipe_id: str,
                                   x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    if not x_user_id:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"errorCode": constants.ErrorCodes.UNAUTHORIZED_REQUEST.value})

    if x_user_id != user_id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content={"errorCode": constants.ErrorCodes.FORBIDDEN_REQUEST.value})

    try:
        services.remove_recipe_from_saved(user_id, recipe_id)
    except (exceptions.RecipeSaverException,) as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,) as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": constants.ErrorCodes.SERVER_ERROR.value})


if __name__ == "__main__":
    uvicorn.run(app, host=constants.HOST, port=constants.PORT)
