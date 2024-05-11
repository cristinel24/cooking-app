import os
from dotenv import load_dotenv
from fastapi import FastAPI, status, Response
import uvicorn
import services
import exceptions
import constants

load_dotenv()

app = FastAPI()


@app.get("/tag")
async def get_tags(starting_with: str, response: Response):
    try:
        return await services.get_tags_by_starting_string(starting_with)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": constants.ErrorCodes.SERVER_ERROR.value}


@app.post("/tag/{name}")
async def add_tag(name: str, response: Response):
    try:
        await services.add_tag_by_name(name)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": constants.ErrorCodes.SERVER_ERROR.value}


@app.delete("/tag/{name}")
async def remove_tag(name: str, response: Response):
    try:
        await services.remove_tag_by_name(name)
    except exceptions.TagException as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"errorCode": e.error_code}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": constants.ErrorCodes.SERVER_ERROR.value}


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST", "localhost"), port=int(os.getenv("PORT", 8000)))
