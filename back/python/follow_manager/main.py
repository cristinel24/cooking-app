from fastapi import FastAPI

import services
from constants import HOST_URL, PORT
from schemas import AuthFollowData


app = FastAPI()


@app.get("/user/{userId}/followers/count", tags=["followers"])
async def get_followers_count(user_id: str) -> dict:
    return await services.get_follower_count(user_id)


@app.get("/user/{userId}/followers", tags=["followers"])
async def get_followers(user_id: str, start: int, count: int) -> dict:
    pass


@app.get("/user/{userId}/following/count", tags=["following"])
async def get_following_count(user_id: str) -> dict:
    return await services.get_following_count(user_id)


@app.get("/user/{userId}/following", tags=["following"])
async def get_following(user_id: str, start: int, count: int) -> dict:
    pass


@app.put("/user/{userId}/following", tags=["auth", "following"])
async def add_follow(auth_follow_data: AuthFollowData) -> dict:
    pass


@app.delete("/user/{userId}/following", tags=["auth", "following"])
async def delete_follow(auth_follow_data: AuthFollowData) -> dict:
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST_URL, port=PORT)
