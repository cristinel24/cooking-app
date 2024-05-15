from fastapi import FastAPI, status
from pymongo import response
from recipe_retriever import exceptions
import services
import uvicorn
from constants import *
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


@app.get("/recipe/{recipe_id}", tags=["recipe-retriever"])
async def get_recipe_by_id(recipe_id: str):
    try:
        return services.get_recipe_by_id(recipe_id)
    except exceptions.RecipeException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"errorCode": e.error_code}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}

@app.get("/recipe/{recipe_id}/card", tags=["recipe-retriever"])
async def get_recipe_card_by_id(recipe_id: str):
    try:
        return services.get_recipe_card_by_id(recipe_id)
    except exceptions.RecipeException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"errorCode": e.error_code}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST_URL, port=PORT)
