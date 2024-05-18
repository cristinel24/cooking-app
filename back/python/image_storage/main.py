import fnmatch
import json
import os.path

from fastapi import FastAPI, UploadFile, Response, status
from fastapi.responses import FileResponse

import services
from constants import HOST_URL, PORT, IMAGE_DIRECTORY_PATH, ErrorCodes
from exception import ImageStorageException

app = FastAPI()


@app.put("/")
async def add_image(file: UploadFile):
    try:
        return await services.add_image(file)
    except ImageStorageException as e:
        return Response(status_code=e.status_code, content=json.dumps({"errorCode": e.error_code}))


@app.get("/{image_id}", response_class=FileResponse)
async def get_image(image_id: str):
    matches = fnmatch.filter(os.listdir(IMAGE_DIRECTORY_PATH), image_id + ".*")
    if matches:
        return IMAGE_DIRECTORY_PATH + matches[0]
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND,
                        content=json.dumps({"errorCode": ErrorCodes.NONEXISTENT_IMAGE.value}))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST_URL, port=PORT)
