"""
USAGE: pytest tests/test_routes/test_user_destroyer_routes.py
Tested: exceptions: invalid user
All tests passed in ~1.0 seconds
CASES TESTED: INVALID USER (USER NONEXISTENT)

ADD TO REQUIREMENTS.TXT:
pytest==7.1.3
httpx==0.23.0
pytest-asyncio==0.19.0
"""

import os
import sys
from unittest.mock import patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from user_destroyer.main import app
from user_destroyer.constants import ErrorCodes
from user_destroyer.services import UserDestroyerException

client = TestClient(app)

VALID_USER = "f"
NONEXISTENT_USER = "nonexistent_user"

USER_DESTROYER_ROUTE = "/{user_id}"

VALID_URL = f"{USER_DESTROYER_ROUTE.format(user_id=VALID_USER)}"
NONEXISTENT_USER_URL = f"{USER_DESTROYER_ROUTE.format(user_id=NONEXISTENT_USER)}"


@patch("user_destroyer.services.delete_user")
def test_nonexistent_user(mock_delete_user):
    mock_delete_user.side_effect = UserDestroyerException(ErrorCodes.NONEXISTENT_USER, 404)

    response = client.delete(NONEXISTENT_USER_URL)
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"errorCode": ErrorCodes.NONEXISTENT_USER.value}


if __name__ == "__main__":
    pytest.main()
