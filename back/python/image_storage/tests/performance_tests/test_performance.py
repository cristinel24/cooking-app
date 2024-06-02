import pytest
import httpx
import asyncio
from fastapi import status

IMAGE_STORAGE_ROUTE = "/"
IMAGE_PATH = "tests/Desktop/Screenshot at 2024-06-01 20-12-54.png"

@pytest.mark.asyncio
async def test_performance_single_request():
    async with httpx.AsyncClient() as client:
        with open(IMAGE_PATH, "rb") as image:
            response = await client.post(IMAGE_STORAGE_ROUTE, files={"file": image}, headers={"x-user-id": "test_user"})
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_performance_multiple_requests(benchmark):
    async def make_request(client):
        with open(IMAGE_PATH, "rb") as image:
            response = await client.post(IMAGE_STORAGE_ROUTE, files={"file": image}, headers={"x-user-id": "test_user"})
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

if __name__ == "__main__":
    pytest.main()