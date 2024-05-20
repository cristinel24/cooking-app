import time

from fastapi import FastAPI, Response, status

from constants import WAIT_ON_ERROR, Errors, HOST, PORT
from exceptions import LoginException
from schemas import LoginData
import service


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
                response.status_code = status.HTTP_401_UNAUTHORIZED
            case Errors.DB_TIMEOUT:
                response.status_code = status.HTTP_504_GATEWAY_TIMEOUT
            case _:
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        # calculez cat timp a trecut, si astept restul de timp
        time_passed = time.time() - time_start
        time.sleep(WAIT_ON_ERROR - time_passed)
        response.status_code = e.http_code
        return {
            "errorCode": e.error_code,
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
