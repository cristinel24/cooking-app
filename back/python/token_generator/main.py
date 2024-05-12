import os
from dotenv import load_dotenv
from fastapi import FastAPI, Response, status
from constants import Errors
import services

load_dotenv()

HOST = os.getenv("TOKEN_GENERATOR_URL", "localhost")
PORT = int(os.getenv("PORT", "8090"))

app = FastAPI()


@app.get("/{user_id}/{token_type}")
async def get_user_token(user_id, token_type, response: Response):
    try:
        token = services.insert_user_token(user_id, token_type)
        return token
    except services.TokenException as e:
        match e.error_code:
            case Errors.INVALID_TYPE:
                response.status_code = status.HTTP_400_BAD_REQUEST
            case Errors.USER_NOT_FOUND:
                response.status_code = status.HTTP_404_NOT_FOUND
            case Errors.DB_TIMEOUT:
                response.status_code = status.HTTP_504_GATEWAY_TIMEOUT
            case _:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": e.error_code}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
