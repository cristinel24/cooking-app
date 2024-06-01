import os
import pathlib
from io import BytesIO

import uuid6
from PIL import Image
from fastapi import UploadFile

from constants import IMAGE_DIRECTORY_PATH, MAX_IMAGE_SIZE, ACCEPTED_IMAGE_EXTENSIONS, ErrorCodes, IMAGE_URL_HEAD
from exception import ImageStorageException


async def add_image(file: UploadFile) -> str:
    image_bytes = BytesIO(await file.read())
    if not file.size:
        raise ImageStorageException(ErrorCodes.INVALID_IMAGE.value, 400)

    if file.size > MAX_IMAGE_SIZE:
        raise ImageStorageException(ErrorCodes.TOO_LARGE_FILE.value, 413)
    try:
        with Image.open(image_bytes) as image:
            image.verify()
    except (IOError, SyntaxError):
        raise ImageStorageException(ErrorCodes.INVALID_IMAGE.value, 400)
    try:
        image_id = str(uuid6.uuid7())
        image = Image.open(image_bytes)
        image.save(IMAGE_DIRECTORY_PATH + image_id + file_extension)
        return IMAGE_URL_HEAD + image_id
            if image.format not in ACCEPTED_IMAGE_FORMATS:
                raise ImageStorageException(ErrorCodes.INVALID_IMAGE_FORMAT.value, 415)
    except UnidentifiedImageError:
        raise ImageStorageException(ErrorCodes.INVALID_IMAGE_FORMAT.value, 415)
    except OSError:
        raise ImageStorageException(ErrorCodes.DUPLICATE_ID.value, 400)
