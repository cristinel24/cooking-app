from fastapi import FastAPI, status, Response
import uvicorn
from dotenv import load_dotenv
from schemas import *
from repository import *
from services import *

load_dotenv()

app = FastAPI()

@app.delete("/recipe/{recipe_id}")
async def delete_recipe(recipe_id,  response: Response):
    try:
        res= await delete_recipe_service(recipe_id)
        if res != 0:
            if res.value == ErrorCodes.RECIPE_NOT_FOUND.value:
                response.status_code = status.HTTP_404_NOT_FOUND
            return { "errorCode" : res }
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return { "errorCode": ErrorCodes.SERVER_ERROR.value }
        

if __name__ == "__main__":
   uvicorn.run(app, host=os.getenv("HOST", "localhost"), port=int(os.getenv("PORT", 8000)))