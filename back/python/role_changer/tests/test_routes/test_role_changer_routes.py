"""
USAGE: pytest tests/test_routes/test_role_changer_routes.py
Tested: exceptions: invalid users, invalid roledata type
All tests passed ~1.0 seconds

ADD TO REQUIREMENTS.TXT
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
from services import RoleChangerException
from schemas import RoleData

client = TestClient(app)

VALID_USER = "1"
NONEXISTENT_USER = "ala bala portocala"

ROLE_CHANGER_ROUTE = "/{user_id}/roles"

VALID_URL = ROLE_CHANGER_ROUTE.format(user_id=VALID_USER)
NONEXISTENT_USER_URL = ROLE_CHANGER_ROUTE.format(user_id=NONEXISTENT_USER)


@patch("services.update_user_roles")
def test_nonexistent_user(mock_update_user_roles):
    mock_update_user_roles.side_effect = RoleChangerException(ErrorCodes.NONEXISTENT_USER.value, status.HTTP_404_NOT_FOUND)

    role_data = {
        "verified": 1,
        "admin": 0,
        "premium": 0,
        "banned": 0
    }

    response = client.put(NONEXISTENT_USER_URL, json=role_data)
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"errorCode": ErrorCodes.NONEXISTENT_USER.value}

@patch("services.update_user_roles")
def test_invalid_role_data_type(mock_update_user_roles):
    role_data = {
        "verified": "john", ### in cazul in care stringul este un numar de exemplu "123" merge sau daca e un numar diferit de -1, 0, 1 se intampla urmatoarele: daca e un numar >0 atunci o sa puna 1 la rol, daca este <0, rolul devine 0
        "admin": 0,
        "premium": 0,
        "banned": 0
    }

    response = client.put(VALID_URL, json=role_data)
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


if __name__ == "__main__":
    pytest.main()
