from typing import Annotated

from fastapi import FastAPI, Response, status, Header

from exception import UserRetrieverException

import services
import uvicorn
from constants import HOST, PORT, ErrorCodes
from schemas import UserData, UserCardData, UserCardsRequestData, UserFullData

app = FastAPI()


@app.get("/user/{user_id}", tags=["user_data"])
async def get_user_data(user_id: str, response: Response) -> UserData | dict[str, int]:
    try:
        return await services.get_user_data(user_id)
    except UserRetrieverException as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code.value}


@app.get("/user/{user_id}/card", tags=["user_card_data"])
async def get_user_card(user_id: str, response: Response) -> UserCardData | dict[str, int]:
    try:
        return await services.get_user_card_data(user_id)
    except UserRetrieverException as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code.value}


@app.post("/user-cards", tags=["user_cards_data"])
async def get_user_cards(user_ids: UserCardsRequestData, response: Response) -> dict[str, list[UserCardData]] | dict[
    str, int]:
    try:
        return {"cards": await services.get_user_cards_data(user_ids.ids)}
    except UserRetrieverException as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code.value}


@app.get("/user/{user_id}/profile", tags=["user_full_data, auth"])
async def get_user_full_data(user_id: str, response: Response,
                             x_user_id: Annotated[str | None, Header()] = None) -> UserFullData | dict[str, int]:
    try:
        if user_id != x_user_id:
            raise UserRetrieverException(status.HTTP_403_FORBIDDEN, ErrorCodes.NOT_AUTHENTICATED)
        return await services.get_user_full_data(user_id)
    except UserRetrieverException as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code.value}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
