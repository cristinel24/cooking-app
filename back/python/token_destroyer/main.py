import services
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from constants import *
from exception import TokenDestroyerException

app = FastAPI(title="Token Destroyer")


@app.delete("/{token}", response_model=None, response_description="Successful operation")
async def delete_token(token: str) -> None | JSONResponse:
    try:
        await services.delete_token(token)
    except TokenDestroyerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.UNKNOWN.value})

@app.delete("/{user_id}/all", response_model=None, response_description="Successful operation")
async def delete_user_tokens(user_id: str) -> None | JSONResponse:
    try:
        await services.delete_user_tokens(user_id)
    except TokenDestroyerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.UNKNOWN.value})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
