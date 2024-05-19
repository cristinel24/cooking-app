import uvicorn
from fastapi import FastAPI, Response, status

from constants import PORT, HOST, ErrorCode
from exceptions import *
from services import get_next_id_services

app = FastAPI()


@app.get("/")
async def get_id(response: Response):
    try:
        new_id = get_next_id_services()
        return new_id
    except IdGeneratorException as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code}
    except (Exception,):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCode.UNKNOWN}


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
