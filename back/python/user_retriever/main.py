from typing import Annotated
from fastapi import FastAPI, Response, status, Header
from fastapi.responses import JSONResponse
from exception import UserRetrieverException
import services
import uvicorn
from constants import HOST, PORT, ErrorCodes
from schemas import UserData, UserCardData, UserCardsRequestData, UserFullData, UserCardDataList

app = FastAPI(title="User Retriever")


@app.get("/{user_id}", tags=["user_data"], response_model=UserData, response_description="Successful operation")
async def get_user_data(user_id: str) -> UserData | JSONResponse:
    try:
        return await services.get_user_data(user_id)
    except UserRetrieverException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.get("/{user_id}/card", tags=["user_card_data"], response_model=UserCardData,
         response_description="Successful operation")
async def get_user_card(user_id: str) -> UserCardData | JSONResponse:
    try:
        return await services.get_user_card_data(user_id)
    except UserRetrieverException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.post("/user-cards", tags=["user_cards_data"], response_model=UserCardDataList,
          response_description="Successful operation")
async def get_user_cards(user_ids: UserCardsRequestData) -> UserCardDataList | JSONResponse:
    try:
        cards = await services.get_user_cards_data(user_ids.ids)
        return UserCardDataList(cards=cards)
    except UserRetrieverException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.get("/user/{user_id}/profile", tags=["user_full_data, auth"], response_model=UserFullData,
         response_description="Successful operation")
async def get_user_full_data(user_id: str,
                             x_user_id: Annotated[str | None, Header()] = None) -> UserFullData | JSONResponse:
    try:
        if user_id != x_user_id:
            raise UserRetrieverException(status.HTTP_403_FORBIDDEN, ErrorCodes.UNAUTHORIZED.value)
        return await services.get_user_full_data(user_id)
    except UserRetrieverException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
