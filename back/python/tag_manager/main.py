import exceptions
import services
import uvicorn
from constants import HOST, PORT, ErrorCodes
from fastapi import FastAPI, Response, status

app = FastAPI()


@app.get("/tag")
async def get_tags(response: Response, starting_with: str = ''):
    try:
        return await services.get_tags_by_starting_string(starting_with)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


@app.post("/tag/{name}")
async def add_tag(name: str, response: Response):
    try:
        await services.add_tag_by_name(name)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


@app.post("/tags")
async def add_tags(names: list[str], response: Response):
    try:
        await services.add_tags(names)
    except exceptions.TagException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"errorCode": e.error_code}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


@app.delete("/tag/{name}")
async def remove_tag(name: str, response: Response):
    try:
        await services.remove_tag_by_name(name)
    except exceptions.TagException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"errorCode": e.error_code}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


@app.patch("/tags")
async def decrement_tags(names: list[str], response: Response):
    try:
        await services.decrement_tags(names)
    except exceptions.TagException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"errorCode": e.error_code}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
