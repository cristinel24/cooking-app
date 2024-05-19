import uvicorn
from dotenv import load_dotenv
from fastapi import status, FastAPI, Request, Response

from recipe_saver import services, constants, exceptions

load_dotenv()
app = FastAPI()


@app.put("/user/{user_id}/saved-recipes", tags=["user-actions"])
async def save_recipe(request: Request, user_id: str, recipe_id: str, response: Response):
    try:
        if not request.state.user_id == user_id:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"errorCode": constants.ErrorCodes.WRONG_USER_ID.value}
        services.save_recipe(user_id, recipe_id)
    except (exceptions.RecipeSaverException,) as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code.value}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": constants.ErrorCodes.SERVER_ERROR.value}


@app.delete("/user/{user_id}/saved-recipes", tags=["user-actions"])
async def remove_recipe_from_saved(request: Request, user_id: str, recipe_id: str, response: Response):
    try:
        if not request.state.user_id == user_id:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"errorCode": constants.ErrorCodes.WRONG_USER_ID.value}
        services.remove_recipe_from_saved(request.state.user_id, recipe_id)
    except (exceptions.RecipeSaverException,) as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code.value}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": constants.ErrorCodes.SERVER_ERROR.value}


if __name__ == "__main__":
    uvicorn.run(app, host=constants.HOST, port=constants.PORT)
