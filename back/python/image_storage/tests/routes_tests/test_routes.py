import os
import sys
from unittest.mock import patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from main import app
from constants import ErrorCodes
from exception import ImageStorageException
from services import add_image

client = TestClient(app)

VALID_USER_ID = "test_user"
INVALID_USER_ID = None
IMAGE_PATH = os.path.join(os.path.dirname(__file__), '../Screenshot at 2024-06-01 20-12-54.png')
IMAGE_STORAGE_ROUTE = "/"


@patch("services.add_image")
def test_add_image_unauthorized(mock_add_image):
    with open(IMAGE_PATH, "rb") as image:
        response = client.post(IMAGE_STORAGE_ROUTE, files={"file": image})
    
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"errorCode": ErrorCodes.UNAUTHORIZED_USER.value}

@patch("services.add_image")
def test_add_image_invalid_extension(mock_add_image):
    mock_add_image.side_effect = ImageStorageException(ErrorCodes.INVALID_IMAGE_EXTENSION.value, 400)

    invalid_image_path = os.path.join(os.path.dirname(__file__), '../tests/invalid_image.txt')

    with open(invalid_image_path, "w") as invalid_image:
        invalid_image.write("This is not a valid image file")

    with open(invalid_image_path, "rb") as image:
        response = client.post(IMAGE_STORAGE_ROUTE, files={"file": image}, headers={"x-user-id": VALID_USER_ID})

    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"errorCode": ErrorCodes.INVALID_IMAGE_EXTENSION.value}

@patch("services.add_image")
def test_add_image_success(mock_add_image):
    mock_add_image.return_value = "http://0.0.0.0:12330/images/test_image_id"

    with open(IMAGE_PATH, "rb") as image:
        response = client.post(IMAGE_STORAGE_ROUTE, files={"file": image}, headers={"x-user-id": VALID_USER_ID})

    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    assert response.status_code == status.HTTP_200_OK
    assert "url" in response.json()

if __name__ == "__main__":
    pytest.main()