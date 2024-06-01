import os
import pathlib
from io import BytesIO

import uuid6
from PIL import Image
from fastapi import UploadFile

from constants import IMAGE_DIRECTORY_PATH, MAX_IMAGE_SIZE, ACCEPTED_IMAGE_EXTENSIONS, ErrorCodes, IMAGE_URL_HEAD
from exception import ImageStorageException


async def add_image(file: UploadFile) -> str:
    if not file.size:
        raise ImageStorageException(ErrorCodes.INVALID_IMAGE.value, 400)

    if file.size > MAX_IMAGE_SIZE:
        raise ImageStorageException(ErrorCodes.TOO_LARGE_FILE.value, 413)

    image_bytes = BytesIO(await file.read())

    try:
        with Image.open(image_bytes) as image:
            if image.format not in ACCEPTED_IMAGE_FORMATS:
                raise ImageStorageException(ErrorCodes.INVALID_IMAGE_FORMAT.value, 415)

            image_id = str(uuid6.uuid7())
            image.save(f"{IMAGE_DIRECTORY_PATH}{image_id}.{image.format.lower()}")

            return f"{IMAGE_URL_HEAD}{image_id}"
    except UnidentifiedImageError:
        raise ImageStorageException(ErrorCodes.INVALID_IMAGE_FORMAT.value, 415)
    except OSError:
        raise ImageStorageException(ErrorCodes.DUPLICATE_ID.value, 400)
    except (IOError, SyntaxError):
        raise ImageStorageException(ErrorCodes.INVALID_IMAGE.value, 400)
