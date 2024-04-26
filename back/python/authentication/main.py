import os
from dotenv import load_dotenv
from fastapi import FastAPI

from authentication.controller import *

load_dotenv()

PORT = int(os.getenv("PORT", "8081"))

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT)
