import uvicorn
from dotenv import load_dotenv
from fastapi import status, FastAPI
from pymongo import response

from recipe_saver import services, constants, exceptions

load_dotenv()
app = FastAPI()


@app.put("/user/{user_id}/saved-recipes", tags=["user-actions"])
async def save_recipe(user_id: str, recipe_id: str):
    try:
        services.save_recipe(user_id, recipe_id)
    except exceptions.RecipeSaverException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"errorCode": e.error_code}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": constants.ErrorCodes.SERVER_ERROR.value}


@app.delete("/user/{user_id}/saved-recipes", tags=["user-actions"])
async def remove_recipe_from_saved(user_id: str, recipe_id: str):
    try:
        services.remove_recipe_from_saved(user_id, recipe_id)
    except exceptions.RecipeSaverException as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"errorCode": e.error_code}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": constants.ErrorCodes.SERVER_ERROR.value}

if __name__ == "__main__":
    uvicorn.run(app, host=constants.HOST_URL, port=constants.PORT)
