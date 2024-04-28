import os

from fastapi import FastAPI
from user.controller import router as user_router
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT", 8000)
HOST = os.getenv("HOST", "0.0.0.0")

app = FastAPI()

app.include_router(user_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
