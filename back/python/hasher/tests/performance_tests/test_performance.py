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


HASH_ALGO_NAME = "argon2"
TARGET_STRING = "teststring"
SALT = "somesalt"

HASH_ALGO_ROUTE = f"http://localhost:12328/{HASH_ALGO_NAME}/{TARGET_STRING}"
PRIMARY_HASH_ALGO_ROUTE = f"http://localhost:12328//{TARGET_STRING}"

@pytest.mark.asyncio
async def test_performance_single_request():
    async with httpx.AsyncClient() as client:
        response = await client.post(HASH_ALGO_ROUTE)
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_performance_multiple_requests(benchmark):
    async def make_request(client):
        response = await client.post(HASH_ALGO_ROUTE)
        assert response.status_code == status.HTTP_200_OK
        return response

    async def run_benchmark():
        async with httpx.AsyncClient() as client:
            tasks = [make_request(client) for _ in range(600)]  # numărul de cereri
            responses = await asyncio.gather(*tasks)
            return responses
        

@pytest.mark.asyncio
async def test_performance_single_request():
    async with httpx.AsyncClient() as client:
        response = await client.post(PRIMARY_HASH_ALGO_ROUTE)
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_performance_multiple_requests(benchmark):
    async def make_request(client):
        response = await client.post(PRIMARY_HASH_ALGO_ROUTE)
        assert response.status_code == status.HTTP_200_OK
        return response

    async def run_benchmark():
        async with httpx.AsyncClient() as client:
            tasks = [make_request(client) for _ in range(600)]  # numărul de cereri
            responses = await asyncio.gather(*tasks)
            return responses

    result = await benchmark(run_benchmark)

    for resp in result:
        assert resp.status_code == status.HTTP_200_OK