from fastapi.responses import JSONResponse
import uvicorn
from fastapi import FastAPI, status

import exceptions
from schemas import TagsBody
import services
from constants import HOST, PORT, ErrorCodes

app = FastAPI(title="Tag Manager")


@app.get("/tag", response_model=TagsBody, response_description="Successful operation")
async def get_tags(starting_with: str = '') -> TagsBody | JSONResponse:
    try:
        tags = await services.get_tags_by_starting_string(starting_with)
        return TagsBody(tags=tags)
    except (Exception,) as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.SERVER_ERROR.value})


@app.post("/tag/{name}/inc", response_model=None, response_description="Successful operation")
async def inc_tag(name: str) -> None | JSONResponse:
    try:
        await services.inc_tag(name)
    except (Exception,) as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.SERVER_ERROR.value})



@app.post("/tags/inc", response_model=None, response_description="Successful operation")
async def inc_tags(body: TagsBody) -> None | JSONResponse:
    try:
        await services.inc_tags(body.tags)
    except (Exception,) as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.SERVER_ERROR.value})



@app.post("/tag/{name}/dec", response_model=None, response_description="Successful operation")
async def dec_tag(name: str) -> None | JSONResponse:
    try:
        await services.dec_tag(name)
    except exceptions.TagException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"errorCode": e.error_code})
    except (Exception,) as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.SERVER_ERROR.value})



@app.post("/tags/dec", response_model=None, response_description="Successful operation")
async def dec_tags(body: TagsBody) -> None | JSONResponse:
    try:
        await services.dec_tags(body.tags)
    except (Exception,) as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.SERVER_ERROR.value})



if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
