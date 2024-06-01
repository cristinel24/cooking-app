"""
USAGE: pytest tests/test_routes/test_hasher_routes
Tested: exception: test_hash_primary_algo error
Result: error assert 500 == 450

ADD TO REQUIREMENTS.TXT
pytest==7.1.3
httpx==0.23.0
pytest-asyncion==0.19.0

"""

import os
import sys
from unittest.mock import patch
import pytest
from fastapi import status
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from main import app
from constants import ErrorCodes
from services import handle_hash_with_primary_algo, handle_hash_with_specific_algo
from schemas import HashData, PrimaryHashData

client = TestClient(app)

HASH_ALGO_NAME = "argon2"
TARGET_STRING = "teststring"
SALT = "somesalt"

HASH_ALGO_ROUTE = f"/{HASH_ALGO_NAME}/{TARGET_STRING}"
PRIMARY_HASH_ALGO_ROUTE = f"/{TARGET_STRING}"

@patch("services.handle_hash_with_primary_algo")
def test_hash_with_primary_algo_error(mock_handle_hash_with_primary_algo):
    mock_handle_hash_with_primary_algo.side_effect = Exception(ErrorCodes.HASH_ALGO_NOT_SUPPORTED.value)
    response = client.get(PRIMARY_HASH_ALGO_ROUTE)
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.json() == {"errorCode": ErrorCodes.HASH_ALGO_NOT_SUPPORTED.value}

if __name__ == "__main__":
    pytest.main()
