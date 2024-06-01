"""
USAGE: pytest tests/test_routes/test_login_routes.py
Tested: exceptions: invalid user
All tests: ~6.0 seconds

ADD TO REQUIREMENTS:
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

from main import app
from constants import Errors
from service import LoginException
from schemas import LoginData

client = TestClient(app)


LOGIN_ROUTE = "/"


@patch("service.login")
def test_nonexistent_user(mock_login):
    mock_login.side_effect = LoginException(Errors.UNKNOWN, status.HTTP_500_INTERNAL_SERVER_ERROR)

    login_data = {
        "identifier":"boss",
        "password":"suntsmechercuvaloare"
    }

    response = client.post(LOGIN_ROUTE, json=login_data)
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"errorCode": Errors.UNKNOWN}


if __name__ == "__main__":
    pytest.main()
