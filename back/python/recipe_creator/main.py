import json

from fastapi import FastAPI, Response

import services
from constants import HOST_URL, PORT
from exception import RecipeCreatorException
from schemas import RecipeData

app = FastAPI()


@app.post("/recipe")
async def create_recipe(recipe_data: RecipeData):
    # todo: add auth request instead of RecipeData
    try:
        await services.create_recipe(recipe_data)
    except RecipeCreatorException as e:
        return Response(status_code=e.status_code, content=json.dumps({"errorCode": e.error_code}))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST_URL, port=PORT)
