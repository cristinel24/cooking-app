from fastapi import FastAPI, Query, Request, status
from fastapi.responses import JSONResponse

from exceptions import *
from schemas import RatingList, RatingCreate, RatingUpdate, RatingDataCard
from services import RatingService

app = FastAPI(title="Rating Manager")

rating_service = RatingService()


@app.middleware("http")
async def normalize_error(request: Request, call_next):
    try:
        response = await call_next(request)
        if response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            response = JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"errorCode": InvalidDataError().value}
            )
    except (DatabaseError, ExternalError, InternalError) as e:
        response = JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"errorCode": e.value}
        )
    except DatabaseNotFoundDataError as e:
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"errorCode": e.value}
        )
    return response


@app.get("/{parent_id}/replies", response_model=RatingList, response_description="Successful operation")
async def get_ratings(parent_id: str, start: int = Query(0), count: int = Query(10)) -> RatingList:
    return await rating_service.get_ratings(parent_id, start, count)


@app.post("/{parent_id}/replies", response_model=RatingDataCard, response_description="Successful operation")
async def create_rating(parent_id: str, rating_data: RatingCreate) -> RatingDataCard:
    return await rating_service.create_rating(parent_id, rating_data)


@app.patch("/{rating_id}", response_model=RatingDataCard, response_description="Successful operation")
async def update_rating(rating_id: str, rating_data: RatingUpdate) -> RatingDataCard:
    return await rating_service.update_rating(rating_id, rating_data)


@app.delete("/{rating_id}", response_model=None, response_description="Successful operation")
async def delete_rating(rating_id: str) -> None:
    return await rating_service.delete_rating(rating_id)
