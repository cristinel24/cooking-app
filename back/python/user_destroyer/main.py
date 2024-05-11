from fastapi import FastAPI

from constants import HOST_URL, PORT

app = FastAPI()


@app.delete("/user/{user_id}", tags=["user-destroyer"])
async def delete_user(user_id: str):
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST_URL, port=PORT)
