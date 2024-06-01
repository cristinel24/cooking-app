"""
USAGE: pytest tests/test_performance/test_performance.py
Tested: performance 
All tests passed between ~1.0 seconds to ~3 minutes (for 1000 requests I used a timeout of 200 seconds)

ADD TO REQUIREMENTS.TXT
pytest==7.1.3
httpx==0.23.0
pytest-asyncio==0.19.0

"""


import pytest
import httpx
import asyncio
from fastapi import status


ROLE_CHANGER_ROUTE = "/{user_id}/roles"

USER_ID = "1"
URL = f"{ROLE_CHANGER_ROUTE.format(user_id=USER_ID)}"

role_data = {
    "verified": -1,
    "admin": -1,
    "premium": -1,
    "banned": -1
}

@pytest.mark.asyncio
async def test_performance_single_request():
    async with httpx.AsyncClient() as client:
        response = await client.put(URL, json=role_data)
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_performance_multiple_requests(benchmark):
    async def make_request(client):
        response = await client.put(URL, json=role_data)
        assert response.status_code == status.HTTP_200_OK
        return response

    async def run_benchmark():
        async with httpx.AsyncClient() as client:
            tasks = [make_request(client) for _ in range(1000)]  # numărul de cereri
            responses = await asyncio.gather(*tasks)
            return responses

    result = await benchmark(run_benchmark)

    for resp in result:
        assert resp.status_code == status.HTTP_200_OK
