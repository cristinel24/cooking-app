from typing import Union

from fastapi import FastAPI, status, Response
from recipe_retriever import exceptions
import services
import uvicorn
from constants import *
from recipe_retriever.schemas import *

app = FastAPI()


@app.get("/recipe/{recipe_id}", tags=["recipe-retriever"])
async def get_recipe_by_id(recipe_id: str, response: Response) -> Union[RecipeData, dict[str, int]]:
    try:
        return await services.get_recipe_by_id(recipe_id)
    except (exceptions.RecipeException, exceptions.UserRetrieverException,) as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code.value}
    except (Exception,) as e:
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


@app.get("/recipe/{recipe_id}/card", tags=["recipe-retriever"])
async def get_recipe_card_by_id(recipe_id: str, response: Response) -> Union[RecipeCardData, dict[str, int]]:
    try:
        return await services.get_recipe_card_by_id(recipe_id)
    except (exceptions.RecipeException, exceptions.UserRetrieverException,) as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code.value}
    except (Exception,) as e:
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST_URL, port=PORT)
