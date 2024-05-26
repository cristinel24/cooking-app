from typing import Annotated
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.params import Header
import uvicorn
from repository import *
from services import *
from constants import *

app = FastAPI(title="Recipe Destroyer")

@app.delete("/recipe/{recipe_id}", tags=["recipe-destroyer"], response_model=None, response_description="Succesful operation")
async def delete_recipe(recipe_id: str, x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    
    if not x_user_id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"errorCode": ErrorCodes.NOT_AUTHENTICATED.value})

    try:
        await delete_recipe_service(recipe_id, x_user_id)
    except RecipeDestroyerException as e:
        return JSONResponse(status_code= e.status_code, content={"errorCode": e.error_code})
        

if __name__ == "__main__":
   uvicorn.run(app, HOST, PORT)