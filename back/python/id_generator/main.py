from fastapi import FastAPI
from constants import ErrorCode
from services import get_next_id_services
from exceptions import *
from dotenv import load_dotenv
import uvicorn
import os

app = FastAPI()

load_dotenv()
PORT = int(os.getenv("PORT", 12345))

@app.get("/")
async def get_id():
    try:
        new_id = get_next_id_services()
        return new_id
    except Exception as e:
        error_code = ErrorCode.DB_ERROR_ID_GENERATOR.value
        error_message = {"errorCode": error_code}
        if isinstance(e, CustomException):
            status_code = e.status_code
        else:
            status_code = 500  # Internal Server Error
        raise HTTPException(status_code=status_code, detail=str(e), headers=error_message)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=PORT, reload=True)
