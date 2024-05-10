from fastapi import FastAPI

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
    pass


@app.put("/user/{user_id}/following", tags=["auth", "following"])
async def add_follow(user_id: str, auth_follow_data: AuthFollowData) -> dict:
    pass


@app.delete("/user/{user_id}/following", tags=["auth", "following"])
async def delete_follow(user_id: str, auth_follow_data: AuthFollowData) -> dict:
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST_URL, port=PORT)
