from fastapi.responses import JSONResponse

from constants import *
from exceptions import TokenException
from fastapi import FastAPI, status
from schemas import TokenData
from services import get_token

app = FastAPI(title="Token Validator")


@app.get("/{token_type}/{token}", response_model=TokenData, response_description="Successful operation")
async def is_valid_token(token_type: str, token: str) -> TokenData | JSONResponse:
    try:
        res = get_token(token, token_type)
        return TokenData(**res)
    except TokenException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": Errors.UNKNOWN})


@app.get("/{token}", response_model=TokenData, response_description="Successful operation")
async def token_exists(token: str) -> TokenData | JSONResponse:
    try:
        res = get_token(token)
        return TokenData(**res)
    except TokenException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": Errors.UNKNOWN})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
