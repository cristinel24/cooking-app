import os

from fastapi import FastAPI
from dotenv import load_dotenv
from services import delete_token
from constants import ErrorCodes
load_dotenv()

PORT = os.getenv("PORT", 8000)
HOST = os.getenv("HOST", "0.0.0.0")

app = FastAPI()


@app.delete("/{token}")
async def delete_token_route(token: str):
    try:
        return await delete_token(token)
    except Exception:
        raise Exception(ErrorCodes.FAILED_TO_RETURN_A_STATUS)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)