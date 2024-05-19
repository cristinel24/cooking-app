import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from constants import *
from services import delete_token
from exception import TokenDestroyerException

app = FastAPI()


@app.delete("/{token}")
async def delete_token_route(token: str):
    try:
        await delete_token(token)
    except TokenDestroyerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)