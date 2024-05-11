import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from schemas import AccountVerification, ChangeRequest
from services import handle_account_verification, handle_change_request

load_dotenv()

app = FastAPI()


@app.post("/verify-account")
async def verify_account(account_verification: AccountVerification):
    handle_account_verification(account_verification)
    return {"message": "OK"}


@app.post("/request-change")
async def request_change(change_request: ChangeRequest):
    handle_change_request(change_request)
    return {"message": "OK"}


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST", "localhost"), port=int(os.getenv("PORT", 2060)))
