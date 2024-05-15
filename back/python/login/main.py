import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI, status, Response

from constants import LoginData, WAIT_ON_ERROR
from exceptions import LoginException
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
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        # calculez cat timp a trecut, si astept restul de timp
        time_passed = time.time() - time_start
        time.sleep(WAIT_ON_ERROR - time_passed)
        return {
            "errorCode": e.error_code,
            "errorMessage": e.error_message
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
