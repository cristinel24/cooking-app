import os
from dotenv import load_dotenv
from fastapi import FastAPI, Response

from services import token_is_valid, get_token

load_dotenv()

HOST = os.getenv("TOKEN_VALIDATOR_URL", "localhost")
PORT = int(os.getenv("PORT", "8090"))


app = FastAPI()


@app.get("/{token_type}/{token}")
async def is_valid_token(token_type, token, response = Response):
    res = token_is_valid(token, token_type)
    if "error_code" in res:
        response.status_code = 500
    return res


@app.get("/{token}")
async def token_exists(token, response = Response):
    res = get_token(token)
    if "error_code" in res:
        response.status_code = 500
    return res


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
