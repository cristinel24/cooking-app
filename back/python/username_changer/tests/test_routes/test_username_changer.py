"""
USAGE: pytest tests/test_routes/test_username_changer.py
Tested: exceptions: invalid token and invalid data

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
from constants import ErrorCodes
from services import handle_change_username
from schemas import UsernameChange, TokenValidatorRequestResponse

client = TestClient(app)

USERNAME_CHANGE_ROUTE = "/"

VALID_TOKEN = "tokentokentokentoken1"
INVALID_TOKEN = "invalid_token"
VALID_USER_ID = "1"
VALID_USERNAME = "username1"
INVALID_USERNAME = "inv" 
NEW_USERNAME = "newusername"


@patch("services.request_token_validation")
@patch("services.request_token_destroy")
def test_change_username_invalid_token(mock_request_token_destroy, mock_request_token_validation):
    mock_request_token_validation.side_effect = Exception(ErrorCodes.TOKEN_VALIDATOR_REQUEST_FAILED.value)

    username_change_data = {
        "username": NEW_USERNAME,
        "token": INVALID_TOKEN
    }

    response = client.post(USERNAME_CHANGE_ROUTE, json=username_change_data)
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"errorCode": ErrorCodes.TOKEN_VALIDATOR_REQUEST_FAILED.value}
    mock_request_token_destroy.assert_not_called()

def test_change_username_invalid_data():
    invalid_username_change_data = {
        "username": INVALID_USERNAME, 
        "token": VALID_TOKEN
    }

    response = client.post(USERNAME_CHANGE_ROUTE, json=invalid_username_change_data)
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

if __name__ == "__main__":
    pytest.main()
