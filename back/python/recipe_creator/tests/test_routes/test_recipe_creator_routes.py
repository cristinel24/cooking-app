"""
USAGE: pytest tests/test_routes/test_recipe_creator_routes.py
Tested: exceptions: missing user and invalid data
All tests: error 


ADD TE REQUIREMENTS.TXT
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
from services import RecipeCreatorException
from schemas import RecipeData

client = TestClient(app)


CREATE_RECIPE_ROUTE = "/"

@patch("services.create_recipe")
def test_create_recipe_missing_user_id(mock_create_recipe):
    mock_create_recipe.side_effect = None

    recipe_data = {
        "title": "Test Recipe",
        "description": "This is a test recipe description that is sufficiently long.",
        "prepTime": 10,
        "steps": ["Step 1", "Step 2"],
        "ingredients": ["Ingredient 1", "Ingredient 2"],
        "allergens": ["Allergen 1"],
        "tags": ["Tag 1"],
        "thumbnail": "http://example.com/thumbnail.jpg"
    }

    response = client.post(CREATE_RECIPE_ROUTE, json=recipe_data)
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"errorCode": ErrorCodes.NOT_AUTHENTICATED.value}


@patch("services.create_recipe")
def test_create_recipe_invalid_data(mock_create_recipe):
    mock_create_recipe.side_effect = RecipeCreatorException(ErrorCodes.INVALID_TITLE_SIZE.value, status.HTTP_400_BAD_REQUEST)

    invalid_recipe_data = {
        "title": "Test", 
        "description": "Short desc",
        "prepTime": 3,  
        "steps": [],
        "ingredients": [],
        "allergens": ["Allergen 1"],
        "tags": ["Tag 1"],
        "thumbnail": "http://example.com/thumbnail.jpg"
    }

    headers = {"x-user-id": "test_user_id"}

    response = client.post(CREATE_RECIPE_ROUTE, json=invalid_recipe_data, headers=headers)
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"errorCode": ErrorCodes.INVALID_TITLE_SIZE.value}


if __name__ == "_main_":
    pytest.main()
