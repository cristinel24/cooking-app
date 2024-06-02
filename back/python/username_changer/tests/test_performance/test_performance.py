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

USERNAME_CHANGE_ROUTE = "/"

VALID_TOKEN = "tokentokentokentoken1"
INVALID_TOKEN = "invalid_token"
VALID_USER_ID = "1"
VALID_USERNAME = "username1"
INVALID_USERNAME = "inv" 
NEW_USERNAME = "newusername"



URL="http://localhost:12350"
ROUTE="/"
USERNAME_CHANGE_ROUTE = "/"

VALID_TOKEN = "tokentokentokentoken1"
INVALID_TOKEN = "invalid_token"
VALID_USER_ID = "1"
VALID_USERNAME = "username1"
INVALID_USERNAME = "inv" 
NEW_USERNAME = "newusername"

data={
    "username": NEW_USERNAME,
    "token":INVALID_TOKEN
}

@pytest.mark.asyncio
async def test_performance_single_request():
    async with httpx.AsyncClient() as client:
        response = await client.post(URL+ROUTE, json=data)
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_performance_multiple_requests(benchmark):
    async def make_request(client):
        response = await client.post(URL+ROUTE, json=data)
        assert response.status_code == status.HTTP_200_OK
        return response

    async def run_benchmark():
        async with httpx.AsyncClient() as client:
            tasks = [make_request(client) for _ in range(500)]  # numărul de cereri
            responses = await asyncio.gather(*tasks)
            return responses

    result = await benchmark(run_benchmark)

    for resp in result:
        assert resp.status_code == status.HTTP_200_OK