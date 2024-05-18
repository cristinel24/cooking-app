import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI, Response, status

from constants import WAIT_ON_ERROR, Errors
from exceptions import LoginException
from schemas import LoginData
import service

load_dotenv()

HOST = os.getenv("LOGIN_URL", "localhost")
PORT = int(os.getenv("PORT", "5000"))

app = FastAPI()


@app.post("/")
async def login(data: LoginData, response=Response):
    time_start = time.time()
    try:
        response = service.login(data)
        return response
    except LoginException as e:
        match e.error_code:
            case Errors.INVALID_CREDS:
                response.status_code = status.HTTP_504_GATEWAY_TIMEOUT
            case Errors.DB_TIMEOUT:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            case _:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        # calculez cat timp a trecut, si astept restul de timp
        time_passed = time.time() - time_start
        time.sleep(WAIT_ON_ERROR - time_passed)
        # trimitem error message doar daca avem invalid creds
        if e.error_code == Errors.INVALID_CREDS:
            return {
                "errorCode": e.error_code,
                "errorMessage": e.error_message
            }
        else:
            return Response(content="", status_code=response.status_code)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
