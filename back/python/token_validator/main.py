import os
from typing import Union

from constants import Errors
from dotenv import load_dotenv
from exceptions import TokenException
from fastapi import FastAPI, Response, status
from schemas import TokenData
from services import get_token

load_dotenv()

HOST = os.getenv("TOKEN_VALIDATOR_URL", "localhost")
PORT = int(os.getenv("PORT", 8090))


app = FastAPI()


@app.get("/{token_type}/{token}")
async def is_valid_token(
    token_type: str, token: str, response: Response
) -> Union[TokenData, dict[str, int]]:
    try:
        res = get_token(token, token_type)
        return TokenData(**res)
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
async def token_exists(
    token: str, response: Response
) -> Union[TokenData, dict[str, int]]:
    try:
        res = get_token(token)
        return TokenData(**res)
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
