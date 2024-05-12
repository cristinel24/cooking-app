import json

from fastapi import FastAPI, Response

import services
from constants import HOST_URL, PORT
from exception import FollowManagerException
from schemas import *

app = FastAPI()


@app.get("/user/{user_id}/followers/count", tags=["followers"])
async def get_followers_count(user_id: str):
    try:
        return await services.get_followers_count(user_id)
    except FollowManagerException as e:
        return Response(status_code=e.status_code, content=json.dumps({"errorCode": e.error_code}))


@app.get("/user/{user_id}/followers", tags=["followers"])
async def get_followers(user_id: str, start: int, count: int):
    try:
        return await services.get_followers(user_id, start, count)
    except FollowManagerException as e:
        return Response(status_code=e.status_code, content=json.dumps({"errorCode": e.error_code}))


@app.get("/user/{user_id}/following/count", tags=["following"])
async def get_following_count(user_id: str):
    try:
        return await services.get_following_count(user_id)
    except FollowManagerException as e:
        return Response(status_code=e.status_code, content=json.dumps({"errorCode": e.error_code}))


@app.get("/user/{user_id}/following", tags=["following"])
async def get_following(user_id: str, start: int, count: int):
    try:
        return await services.get_following(user_id, start, count)
    except FollowManagerException as e:
        return Response(status_code=e.status_code, content=json.dumps({"errorCode": e.error_code}))


@app.put("/user/{user_id}/following", tags=["auth", "following"])
async def add_follow(user_id: str, body: FollowData):
    try:
        await services.add_follow(user_id, body.followsId)
    except FollowManagerException as e:
        return Response(status_code=e.status_code, content=json.dumps({"errorCode": e.error_code}))


@app.delete("/user/{user_id}/following", tags=["auth", "following"])
async def delete_follow(user_id: str, body: FollowData):
    try:
        await services.delete_follow(user_id, body.followsId)
    except FollowManagerException as e:
        return Response(status_code=e.status_code, content=json.dumps({"errorCode": e.error_code}))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST_URL, port=PORT)
