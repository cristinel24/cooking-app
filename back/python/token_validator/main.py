import os
from dotenv import load_dotenv
from fastapi import FastAPI
from services import token_is_valid, get_token

load_dotenv()

HOST = os.getenv("TOKEN_VALIDATOR_URL", "localhost")
PORT = int(os.getenv("PORT", "8090"))


app = FastAPI()


@app.get("/{token_type}/{token}")
async def is_valid_token(token_type, token):
    return token_is_valid(token, token_type)


@app.get("/{token}")
async def token_exists(token):
    return get_token(token)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
