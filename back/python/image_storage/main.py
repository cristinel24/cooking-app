import json
import os.path
from io import BytesIO

from fastapi import FastAPI, UploadFile, Response
from fastapi.responses import FileResponse

import services
from constants import HOST_URL, PORT, IMAGE_DIRECTORY_PATH, IMAGE_EXTENSION, ErrorCodes
from exception import ImageStorageException

app = FastAPI()


@app.put("/")
async def add_image(file: UploadFile):
    try:
        return await services.add_image(BytesIO(await file.read()))
    except ImageStorageException as e:
        return Response(status_code=e.status_code, content=json.dumps({"errorCode": e.error_code.value}))


@app.get("/{image_id}", response_class=FileResponse)
async def get_image(image_id: str):
    image_path = IMAGE_DIRECTORY_PATH + image_id + IMAGE_EXTENSION
    if os.path.exists(image_path):
        return image_path
    else:
        return Response(status_code=404, content=json.dumps({"errorCode": ErrorCodes.NONEXISTENT_IMAGE.value}))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST_URL, port=PORT)
