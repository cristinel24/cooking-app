from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import uvicorn
from constants import HOST, PORT, ErrorCodesToHTTPCodesMapping
from schemas import UsernameChange
from services import handle_change_username

app = FastAPI(title="Username Changer")


@app.post("/", response_model=None, response_description="Successful operation")
async def change_username(username_change: UsernameChange) -> None | JSONResponse:
    try:
        handle_change_username(username_change)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_code = int(str(e))
        if error_code in ErrorCodesToHTTPCodesMapping:
            status_code = ErrorCodesToHTTPCodesMapping[error_code]
        return JSONResponse(status_code=status_code, content={"errorCode": error_code})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)