import os
from dotenv import load_dotenv
from fastapi import FastAPI

from authentication.controller import *

load_dotenv()

HOST = os.getenv("AUTH_MODULE_HOST", "localhost")
PORT = int(os.getenv("AUTH_MODULE_PORT", "8082"))

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
