import httpx

from constants import USER_RETRIEVER_API_URL, USER_CARDS_ROUTE
from schemas import *


async def request_user_cards(user_ids: UserCardRequestData) -> UserCardResponseData:
    async with httpx.AsyncClient() as client:
        payload = user_ids.model_dump_json()
        response = await client.post(url=USER_RETRIEVER_API_URL + USER_CARDS_ROUTE,
                                     content=payload)
        user_card_response_data = UserCardResponseData()
        user_card_response_data.cards = response.json()["cards"]
        return user_card_response_data
