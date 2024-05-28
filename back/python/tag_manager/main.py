import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

import services
from constants import HOST, PORT, ErrorCodes
from schemas import TagsBody

app = FastAPI(title="Tag Manager")


@app.get("/", response_model=TagsBody, response_description="Successful operation")
async def get_tags(starting_with: str = '') -> TagsBody | JSONResponse:
    try:
        tags = await services.get_tags_by_starting_string(starting_with)
        return TagsBody(tags=tags)
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": ErrorCodes.SERVER_ERROR.value})


@app.post("/", response_model=None, response_description="Successful operation")
async def update_tags(action: int, body: TagsBody) -> None | JSONResponse:
    try:
        match action:
            case 1:
                await services.inc_tags(body.tags)
            case -1:
                await services.dec_tags(body.tags)
            case _:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content={"errorCode": ErrorCodes.BAD_ACTION.value})
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": ErrorCodes.SERVER_ERROR.value})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
