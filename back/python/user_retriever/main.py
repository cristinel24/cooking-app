from dotenv import load_dotenv
from fastapi import FastAPI

import services
from constants import HOST_URL, PORT
from schemas import UserData, UserCardData, UserFullData

app = FastAPI()

load_dotenv()


@app.get("/user/{user_id}", tags=["user_data"])
async def get_user_data(user_id: str) -> UserData:
    return await services.get_user_data(user_id)


@app.get("/user/{user_id}/card", tags=["user_card_data"])
async def get_user_card(user_id: str) -> UserCardData:
    return await services.get_user_card_data(user_id)


@app.post("/user-cards", tags=["user_cards_data"])
async def get_user_cards(user_ids: list[str]) -> list[UserCardData]:
    return await services.get_user_cards_data(user_ids)


# @app.get("/user/{user_id}/profile", tags=["user_full_data"])
# async def get_user_full_data(user_id: str) -> UserFullData:
#    return await services.get_user_full_data(user_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST_URL, port=PORT)
