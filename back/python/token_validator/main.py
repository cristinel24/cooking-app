from typing import Union

from constants import *
from exceptions import TokenException
from fastapi import FastAPI, Response, status
from schemas import TokenData
from services import get_token

app = FastAPI()


@app.get("/{token_type}/{token}")
async def is_valid_token(
    token_type: str, token: str, response: Response
) -> Union[TokenData, dict[str, int]]:
    try:
        res = get_token(token, token_type)
        return TokenData(**res)
    except TokenException as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code}
    except Exception:
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
        response.status_code = e.status_code
        return {"errorCode": e.error_code}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": Errors.UNKNOWN}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
