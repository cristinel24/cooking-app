import os

from dotenv import load_dotenv
from fastapi import FastAPI, status, Response
from constants import ErrorCodes
from services import delete_token

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")

app = FastAPI()


@app.delete("/{token}")
async def delete_token_route(token: str):
    try:
        await delete_token(token)
    except Exception as e:
        Response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)