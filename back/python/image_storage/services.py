import os
from io import BytesIO

from PIL import Image

from constants import IMAGE_DIRECTORY_PATH, IMAGE_EXTENSION, ErrorCodes

counter = 0


async def add_image(image_bytes: BytesIO):
    if not os.path.exists(IMAGE_DIRECTORY_PATH):
        os.mkdir(IMAGE_DIRECTORY_PATH)
    try:
        with Image.open(image_bytes) as image:
            image.verify()
    except (IOError, SyntaxError):
        raise Exception(ErrorCodes.INVALID_IMAGE.value)
    image = Image.open(image_bytes)
    image.save(IMAGE_DIRECTORY_PATH + str(counter + 1) + IMAGE_EXTENSION)
