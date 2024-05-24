from fastapi.responses import JSONResponse
import uvicorn
from fastapi import status, FastAPI, Request

from schemas import RecipeId
import services, constants, exceptions

app = FastAPI(title="Recipe Saver")


@app.put("/{user_id}/saved-recipes", tags=["user-actions"], response_model=None, response_description="Successful operation")
async def save_recipe(request: Request, user_id: str, data: RecipeId) -> None | JSONResponse:
    if not request.state.user_id == user_id:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errorCode": constants.ErrorCodes.WRONG_USER_ID.value})

    try:
        services.save_recipe(user_id, data.id)
    except (exceptions.RecipeSaverException,) as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,) as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": constants.ErrorCodes.SERVER_ERROR.value})


@app.delete("/{user_id}/saved-recipes", tags=["user-actions"], response_model=None, response_description="Successful operation")
async def remove_recipe_from_saved(request: Request, user_id: str, data: RecipeId) -> None | JSONResponse:
    if not request.state.user_id == user_id:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errorCode": constants.ErrorCodes.WRONG_USER_ID.value})

    try:
        services.remove_recipe_from_saved(request.state.user_id, data.id)
    except (exceptions.RecipeSaverException,) as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,) as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": constants.ErrorCodes.SERVER_ERROR.value})


if __name__ == "__main__":
    uvicorn.run(app, host=constants.HOST, port=constants.PORT)
