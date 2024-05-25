import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from constants import HOST, PORT, ErrorCodes
from exception import RegisterException
from schemas import NewUserData
import services

app = FastAPI(title="Register")


@app.post("/", tags=["register"], response_model=None, response_description="Successful operation")
async def register(user_data: NewUserData) -> None | JSONResponse:
    try:
        await services.register(user_data)
    except RegisterException as e:
        return JSONResponse(status_code=e.status_code, content={"error_code": e.error_code})
    except (Exception,) as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error_code": ErrorCodes.SERVER_ERROR.value})


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
