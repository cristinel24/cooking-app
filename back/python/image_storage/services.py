import os
from io import BytesIO

import httpx
from PIL import Image

import api
from constants import IMAGE_DIRECTORY_PATH, IMAGE_EXTENSION, ErrorCodes
from exception import ImageStorageException


async def add_image(image_bytes: BytesIO):
    if not os.path.exists(IMAGE_DIRECTORY_PATH):
        os.mkdir(IMAGE_DIRECTORY_PATH)
    try:
        with Image.open(image_bytes) as image:
            image.verify()
    except (IOError, SyntaxError):
        raise ImageStorageException(ErrorCodes.INVALID_IMAGE, 400)
    try:
        image_id = await api.get_id()
        image = Image.open(image_bytes)
        image.save(IMAGE_DIRECTORY_PATH + image_id + IMAGE_EXTENSION)
    except httpx.ConnectError:
        raise ImageStorageException(ErrorCodes.NOT_RESPONSIVE_API, 404)
    except OSError:
        raise ImageStorageException(ErrorCodes.DUPLICATE_ID, 400)
