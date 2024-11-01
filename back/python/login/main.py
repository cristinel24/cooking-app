import time

import service
from constants import HOST, PORT, WAIT_ON_ERROR, Errors
from exceptions import LoginException
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from schemas import LoginData, LoginResponse

app = FastAPI(title="Login")


@app.post("/", response_model=LoginResponse, response_description="Succesful login")
async def login(data: LoginData) -> LoginResponse | JSONResponse:
    time_start = time.time()
    try:
        response = await service.login(data)
        return LoginResponse(**response)
    except LoginException as e:
        print(e)
        # calculez cat timp a trecut, si astept restul de timp
        time_passed = time.time() - time_start
        time.sleep(WAIT_ON_ERROR - time_passed)
        return JSONResponse(
            status_code=e.http_code, content={"errorCode": e.error_code}
        )
    except Exception as e:
        print(e)
        time_passed = time.time() - time_start
        time.sleep(WAIT_ON_ERROR - time_passed)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"errorCode": Errors.UNKNOWN},
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
