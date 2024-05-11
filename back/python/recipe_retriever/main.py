from bson import ObjectId
from fastapi import FastAPI

import services
from constants import HOST_URL, PORT

app = FastAPI()


@app.get("/recipe/{recipe_id}", tags=["recipe-retriever"])
async def get_recipe_by_id(recipe_id: str):
    return await services.get_recipe_by_id(ObjectId(recipe_id))

@app.get("/recipe/{recipe_id}/card", tags=["recipe-retriever"])
async def get_recipe_card_by_id(recipe_id: str):
    return await services.get_recipe_card_by_id(ObjectId(recipe_id))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST_URL, port=PORT)
