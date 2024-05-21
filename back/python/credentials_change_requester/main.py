from typing import Set, Any

from fastapi import FastAPI,status
import services
import uvicorn
from constants import HOST, PORT, ErrorCodes
from schemas import CredentialChangeRequest

app = FastAPI()


@app.post("/", tags=["credentials_change_requester"])
async def create_request(request: CredentialChangeRequest) -> set[Any]:
        services.create_request(request)
        return {status.HTTP_200_OK}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
