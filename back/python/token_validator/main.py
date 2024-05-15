import os
from dotenv import load_dotenv
from fastapi import FastAPI, Response, status

from services import token_is_valid, get_token
from constants import Errors
from exceptions import TokenException

load_dotenv()

HOST = os.getenv("TOKEN_VALIDATOR_URL", "localhost")
PORT = int(os.getenv("PORT", "8090"))


app = FastAPI()


@app.get("/{token_type}/{token}")
async def is_valid_token(token_type, token, response=Response):
    try:
        res = token_is_valid(token_type, token)
        return res
    except TokenException as e:
        match e.error_code:
            case Errors.INVALID_TYPE:
                response.status_code = status.HTTP_400_BAD_REQUEST
            case Errors.DB_ERROR:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            case Errors.DB_TIMEOUT:
                response.status_code = status.HTTP_504_GATEWAY_TIMEOUT
            case _:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": e.error_code}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": Errors.UNKNOWN}


@app.get("/{token}")
async def token_exists(token, response=Response):
    try:
        res = get_token(token)
        return res
    except TokenException as e:
        match e.error_code:
            case Errors.INVALID_TYPE:
                response.status_code = status.HTTP_400_BAD_REQUEST
            case Errors.DB_ERROR:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            case Errors.DB_TIMEOUT:
                response.status_code = status.HTTP_504_GATEWAY_TIMEOUT
            case _:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": e.error_code}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": Errors.UNKNOWN}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
