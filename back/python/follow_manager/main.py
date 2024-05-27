from typing import Annotated

import services
from constants import HOST, PORT, ErrorCodes
from exception import FollowManagerException
from fastapi import FastAPI, Header, status
from fastapi.responses import JSONResponse
from schemas import *

app = FastAPI(title="Follow Manager")


@app.get("/{user_id}/followers/count", tags=["followers"], response_model=FollowersCountData,
         response_description="Successful operation")
async def get_followers_count(user_id: str) -> FollowersCountData | JSONResponse:
    try:
        return await services.get_followers_count(user_id)
    except FollowManagerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.get("/{user_id}/followers", tags=["followers"], response_model=FollowersCardsData,
         response_description="Successful operation")
async def get_followers(user_id: str, start: int, count: int) -> FollowersCardsData | JSONResponse:
    try:
        return await services.get_followers(user_id, start, count)
    except FollowManagerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.get("/{user_id}/following/count", tags=["following"], response_model=FollowingCountData,
         response_description="Successful operation")
async def get_following_count(user_id: str) -> FollowingCountData | JSONResponse:
    try:
        return await services.get_following_count(user_id)
    except FollowManagerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.get("/{user_id}/following", tags=["following"], response_model=FollowingCardsData,
         response_description="Successful operation")
async def get_following(user_id: str, start: int, count: int) -> FollowingCardsData | JSONResponse:
    try:
        return await services.get_following(user_id, start, count)
    except FollowManagerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.post("/{user_id}/follow", tags=["auth", "follow"], response_model=None,
          response_description="Successful operation")
async def add_follow(user_id: str, body: FollowData,
                     x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    if not x_user_id or user_id != x_user_id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content={"errorCode": ErrorCodes.NOT_AUTHENTICATED.value})
    try:
        await services.add_follow(user_id, body.followsId)
    except FollowManagerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.get("/{user_id}/follow", tags=["follow"], response_model=FollowResponse,
         response_description="Successful operation")
async def get_follow(user_id: str, follows_id: str) -> FollowResponse | JSONResponse:
    try:
        return await services.get_follow(user_id, follows_id)
    except FollowManagerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.delete("/{user_id}/follow", tags=["auth", "follow"], response_model=None,
            response_description="Successful operation")
async def delete_follow(user_id: str, body: FollowData,
                        x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    if not x_user_id or user_id != x_user_id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content={"errorCode": ErrorCodes.NOT_AUTHENTICATED.value})
    try:
        await services.delete_follow(user_id, body.followsId)
    except FollowManagerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
