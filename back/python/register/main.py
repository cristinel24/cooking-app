import os
import uvicorn

from fastapi import FastAPI, Response, status

from constants import  HOST_URL, PORT, ErrorCodes
from exceptions import RegisterException
from schemas import UserCreateData
import service

app = FastAPI()


@app.post("/", tags=["register"])
async def register(user_data: UserCreateData, response: Response) -> dict[str, ErrorCodes] | None:
    try:
        await service.register(user_data)
    except RegisterException as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST_URL, port=PORT)
