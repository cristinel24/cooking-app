import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from authentication.controller import *

load_dotenv()

HOST = os.getenv("AUTH_MODULE_HOST", "localhost")
PORT = int(os.getenv("AUTH_MODULE_PORT", "8082"))

app = FastAPI()

origins = ["http://localhost:5173"]  # TODO: should be replaced with frontend address from env

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
