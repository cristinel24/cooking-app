import services
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from constants import *
from exception import TokenDestroyerException

app = FastAPI()


@app.delete("/{token}")
async def delete_token(token: str):
    try:
        await services.delete_token(token)
    except TokenDestroyerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.UNKNOWN.value})

@app.delete("/{user_id}/all")
async def delete_user_tokens(user_id: str):
    try:
        await services.delete_user_tokens(user_id)
    except TokenDestroyerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.UNKNOWN.value})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
