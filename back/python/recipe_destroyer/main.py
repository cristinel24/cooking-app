from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv
from repository import *
from services import *
from constants import *

load_dotenv()

app = FastAPI(title="Recipe Destroyer")

@app.delete("/recipe/{recipe_id}", tags=["recipe-destroyer"], response_model=None, response_description="Succesful operation")
async def delete_recipe(recipe_id) -> None | JSONResponse:
    try:
        await delete_recipe_service(recipe_id)
        
    except RecipeDestroyerException as e:
        return JSONResponse(status_code= e.status_code, content={"errorCode": e.error_code.value})
        

if __name__ == "__main__":
   uvicorn.run(app, HOST, PORT)