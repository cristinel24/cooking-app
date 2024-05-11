from dotenv import load_dotenv
from fastapi import FastAPI

import services
import uvicorn
from constants import HOST_URL, PORT
from schemas import *
from schemas import UserData
from utils import verify_auth

app = FastAPI()

load_dotenv()


@app.get("/user/{user_id}", tags=["user_data"])
async def get_user_data(user_id: str) -> UserData | ErrorCode:
    try:
        return await services.get_user_data(user_id)
    except Exception as e:
        return ErrorCode(error_code=int(str(e)))


@app.get("/user/{user_id}/card", tags=["user_card_data"])
async def get_user_card(user_id: str) -> UserCardData | ErrorCode:
    try:
        return await services.get_user_card_data(user_id)
    except Exception as e:
        return ErrorCode(error_code=int(str(e)))


@app.post("/user-cards", tags=["user_cards_data"])
async def get_user_cards(user_ids: UserCardsRequestData) -> list[UserCardData] | ErrorCode:
    try:
        return await services.get_user_cards_data(user_ids.ids)
    except Exception as e:
        return ErrorCode(error_code=int(str(e)))


@app.get("/user/{user_id}/profile", tags=["user_full_data, auth"])
async def get_user_full_data(user_id: str, user_roles: int) -> UserFullData | ErrorCode:
    try:
        verify_auth(user_roles)
        return await services.get_user_full_data(user_id)
    except Exception as e:
        return ErrorCode(error_code=int(str(e)))


if __name__ == "__main__":
    uvicorn.run(app, host=HOST_URL, port=PORT)
