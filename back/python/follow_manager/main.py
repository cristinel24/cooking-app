import json
from typing import Annotated

from fastapi import Body, FastAPI, Header, Response, status
from fastapi.responses import JSONResponse

import services
from constants import HOST, PORT, ErrorCodes
from exception import FollowManagerException
from schemas import *

app = FastAPI()


@app.get("/user/{user_id}/followers/count", tags=["followers"])
async def get_followers_count(user_id: str):
    try:
        return await services.get_followers_count(user_id)
    except FollowManagerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.get("/user/{user_id}/followers", tags=["followers"])
async def get_followers(user_id: str, start: int, count: int):
    try:
        return await services.get_followers(user_id, start, count)
    except FollowManagerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.get("/user/{user_id}/following/count", tags=["following"])
async def get_following_count(user_id: str):
    try:
        return await services.get_following_count(user_id)
    except FollowManagerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.get("/user/{user_id}/following", tags=["following"])
async def get_following(user_id: str, start: int, count: int):
    try:
        return await services.get_following(user_id, start, count)
    except FollowManagerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.put("/user/{user_id}/following", tags=["auth", "following"])
async def add_follow(user_id: str, body: FollowData, x_user_id: Annotated[str | None, Header()] = None):
    if not x_user_id or user_id is not x_user_id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"errorCode": ErrorCodes.NOT_AUTHENTICATED.value})
    try:
        await services.add_follow(user_id, body.followsId)
    except FollowManagerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.delete("/user/{user_id}/following", tags=["auth", "following"])
async def delete_follow(user_id: str, body: FollowData, x_user_id: Annotated[str | None, Header()] = None):
    if not x_user_id or user_id is not x_user_id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"errorCode": ErrorCodes.NOT_AUTHENTICATED.value})
    try:
        await services.delete_follow(user_id, body.followsId)
    except FollowManagerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
