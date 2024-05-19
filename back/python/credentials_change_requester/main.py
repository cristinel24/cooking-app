from fastapi import FastAPI, Response, Request, status
from exceptions import CredentialChangeRequesterException
import services
import uvicorn
from constants import HOST, PORT, ErrorCodes
from schemas import CredentialChangeRequest

app = FastAPI()


@app.post("/", tags=["credentials_change_requester"])
async def create_request(request: CredentialChangeRequest, response: Response) -> dict[str, int]:
    try:
        await services.create_request(request)
    except CredentialChangeRequesterException as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code.value}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
