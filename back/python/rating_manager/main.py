import uvicorn
from fastapi import FastAPI, Query, APIRouter, Request, status
from fastapi.responses import JSONResponse

from schemas import RatingList, RatingCreate, RatingUpdate
from services import RatingService
from exceptions import DatabaseError, ExternalError, InternalError, InvalidDataError, DatabaseNotFoundDataError


app = FastAPI()

rating_service = RatingService()


@app.middleware("http")
async def normalize_error(request: Request, call_next):
    try:
        response = await call_next(request)
        if response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            response = JSONResponse(
                status_code=400,
                content={"errorCode": InvalidDataError().value}
            )
    except (DatabaseError, ExternalError, InternalError) as e:
        response = JSONResponse(
            status_code=500,
            content={"errorCode": e.value}
        )
    except DatabaseNotFoundDataError as e:
        response = JSONResponse(
            status_code=404,
            content={"errorCode": e.value}
        )
    return response


@app.get("/rating/{parent_id}/replies", response_model=RatingList, response_description="Successful operation")
async def get_ratings(parent_id: str, start: int = Query(0), count: int = Query(10)) -> RatingList | JSONResponse:
    return await rating_service.get_ratings(parent_id, start, count)


@app.put("/rating/{parent_id}/replies", response_description="Successful operation")
async def create_rating(parent_id: str, rating_data: RatingCreate) -> JSONResponse:
    return await rating_service.create_rating(parent_id, rating_data)


@app.patch("/rating/{rating_id}", response_description="Successful operation")
async def update_rating(rating_id: str, rating_data: RatingUpdate) -> JSONResponse:
    return await rating_service.update_rating(rating_id, rating_data)


@app.delete("/rating/{rating_id}", response_description="Successful operation")
async def delete_rating(rating_id: str) -> JSONResponse:
    return await rating_service.delete_rating(rating_id)

if __name__ == "__main__":
    PORT = int(8001)
    HOST = "127.0.0.1"
    uvicorn.run(app, host=HOST, port=PORT, reload=True)
