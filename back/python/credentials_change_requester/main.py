from typing import Set, Any

from fastapi import FastAPI, status
from starlette.responses import JSONResponse

import services
import uvicorn
from constants import HOST, PORT, ErrorCodes
from exceptions import CredentialChangeRequesterException
from schemas import CredentialChangeRequest
from fastapi.responses import JSONResponse

app = FastAPI(title="Credentials Change Requester")


@app.post("/", tags=["credentials_change_requester"], response_model=None, response_description="Successful operation")
async def create_request(request: CredentialChangeRequest) -> None | JSONResponse:
    try:
        await services.create_request(request)
    except CredentialChangeRequesterException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": ErrorCodes.SERVER_ERROR.value})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
