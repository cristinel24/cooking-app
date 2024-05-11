import os
from dotenv import load_dotenv
from fastapi import FastAPI, Response
from constants import Errors
import services

load_dotenv()

HOST = os.getenv("TOKEN_GENERATOR_URL", "localhost")
PORT = int(os.getenv("PORT", "8090"))

app = FastAPI()


@app.get("/{user_id}/{token_type}")
async def get_user_token(user_id, token_type, response: Response):
    try:
        token = services.get_user_token(user_id, token_type)
        if "error_code" in token:
            if token["error_code"] == Errors.USER_NOT_FOUND:
                response.status_code = 404
            elif token["error_code"] == Errors.INVALID_TYPE:
                response.status_code = 400
        return token
    except Exception as e:
        print(e)
        response.status_code = 500
        return {"error_code": Errors.DATABASE_ERROR}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
