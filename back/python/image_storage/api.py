import httpx

from constants import ID_GENERATOR_API_URL, ID_GENERATOR_ROUTE


async def get_id() -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url=ID_GENERATOR_API_URL + ID_GENERATOR_ROUTE)
        return response.json()["id"]
