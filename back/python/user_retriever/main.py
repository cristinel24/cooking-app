from pymongo import errors
import pymongo
from dotenv import load_dotenv
from fastapi import FastAPI, Response, status

import services
import uvicorn
from constants import HOST_URL, PORT, ErrorCodes
from schemas import UserData, UserCardData, UserCardsRequestData, UserFullData

app = FastAPI()

load_dotenv()


@app.get("/user/{user_id}", tags=["user_data"])
async def get_user_data(user_id: str, response: Response) -> UserData | dict[str, int]:
    try:
        return await services.get_user_data(user_id)
    except pymongo.errors.PyMongoError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.DATABASE_ERROR.value}
    except Exception as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"errorCode": int(str(e))}


@app.get("/user/{user_id}/card", tags=["user_card_data"])
async def get_user_card(user_id: str, response: Response) -> UserCardData | dict[str, int]:
    try:
        return await services.get_user_card_data(user_id)
    except pymongo.errors.PyMongoError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.DATABASE_ERROR.value}
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"errorCode": int(str(e))}


@app.post("/user-cards", tags=["user_cards_data"])
async def get_user_cards(user_ids: UserCardsRequestData, response: Response) -> list[UserCardData] | dict[str, int]:
    try:
        return await services.get_user_cards_data(user_ids.ids)
    except pymongo.errors.PyMongoError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.DATABASE_ERROR.value}
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"errorCode": int(str(e))}


@app.get("/user/{user_id}/profile", tags=["user_full_data, auth"])
async def get_user_full_data(user_id: str, user_roles: int, response: Response) -> UserFullData | dict[str, int]:
    try:
        return await services.get_user_full_data(user_id)
    except pymongo.errors.PyMongoError:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.DATABASE_ERROR.value}
    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"errorCode": int(str(e))}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST_URL, port=PORT)
