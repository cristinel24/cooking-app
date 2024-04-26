import os
from dotenv import load_dotenv
from fastapi import FastAPI

from recipe.controller import *

load_dotenv()

PORT = int(os.getenv("PORT", "8082")) #nu e ca la auth 8081

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)