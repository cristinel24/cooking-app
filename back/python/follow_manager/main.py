from fastapi import FastAPI, Response

import services
from constants import HOST_URL, PORT
from schemas import *

app = FastAPI()


@app.get("/user/{user_id}/followers/count", tags=["followers"])
async def get_followers_count(user_id: str) -> FollowersCountData:
    return await services.get_followers_count(user_id)


@app.get("/user/{user_id}/followers", tags=["followers"])
async def get_followers(user_id: str, start: int, count: int) -> FollowersCardsData:
    return await services.get_followers(user_id, start, count)


@app.get("/user/{user_id}/following/count", tags=["following"])
async def get_following_count(user_id: str) -> FollowingCountData:
    return await services.get_following_count(user_id)


@app.get("/user/{user_id}/following", tags=["following"])
async def get_following(user_id: str, start: int, count: int) -> FollowingCardsData:
    return await services.get_following(user_id, start, count)


@app.put("/user/{user_id}/following", tags=["auth", "following"])
async def add_follow(user_id: str, body: FollowData):
    if not await services.add_follow(user_id, body.followsId):
        return Response(status_code=406)


@app.delete("/user/{user_id}/following", tags=["auth", "following"])
async def delete_follow(user_id: str, body: FollowData):
    if not await services.delete_follow(user_id, body.followsId):
        return Response(status_code=406)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST_URL, port=PORT)
