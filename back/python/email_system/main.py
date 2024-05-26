from fastapi import FastAPI, status, Response
from fastapi.responses import JSONResponse
import uvicorn

from constants import ErrorCodesToHTTPCodesMapping, HOST, PORT
from schemas import AccountVerification, ChangeRequest
from services import handle_account_verification, handle_change_request

app = FastAPI(title="Email System")


@app.post("/verify-account", response_model=None, response_description="Successful operation")
async def verify_account(account_verification: AccountVerification) -> None | JSONResponse:
    try:
        handle_account_verification(account_verification)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_code = int(str(e))
        if error_code in ErrorCodesToHTTPCodesMapping:
            status_code = ErrorCodesToHTTPCodesMapping[error_code]
        return JSONResponse(status_code=status_code, content={"errorCode": error_code})


@app.post("/request-change", response_model=None, response_description="Successful operation")
async def request_change(change_request: ChangeRequest) -> None | JSONResponse:
    try:
        handle_change_request(change_request)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_code = int(str(e))
        if error_code in ErrorCodesToHTTPCodesMapping:
            status_code = ErrorCodesToHTTPCodesMapping[error_code]
        return JSONResponse(status_code=status_code, content={"errorCode": error_code})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
