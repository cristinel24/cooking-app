import os
from dotenv import load_dotenv
from fastapi import FastAPI, status, Response
import uvicorn
from constants import ErrorCodesToHTTPCodesMapping
from schemas import PasswordChange
from services import handle_change_password

load_dotenv()

app = FastAPI()


@app.post("/")
async def change_password(password_change: PasswordChange, response: Response):
    try:
        await handle_change_password(password_change)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_code = int(str(e))
        if error_code in ErrorCodesToHTTPCodesMapping:
            response.status_code = ErrorCodesToHTTPCodesMapping[error_code]
        return {"errorCode": error_code}


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST", "localhost"), port=int(os.getenv("PORT", 2590)))
