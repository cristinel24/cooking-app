from fastapi.responses import JSONResponse
import uvicorn
from fastapi import FastAPI, status

from constants import PORT, HOST, ErrorCode
from exceptions import *
from schemas import Id
from services import get_next_id_services

app = FastAPI(title="Id Generator")


@app.get("/", response_model=Id, response_description="Successful operation")
async def get_id() -> Id | JSONResponse:
    try:
        new_id = get_next_id_services()
        return Id(id=new_id)
    except IdGeneratorException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCode.UNKNOWN})


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
