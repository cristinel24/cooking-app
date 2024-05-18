import fnmatch
import json
import os.path

from fastapi import FastAPI, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse

import services
from constants import HOST, PORT, IMAGE_DIRECTORY_PATH, ErrorCodes
from exception import ImageStorageException

app = FastAPI()


@app.put("/")
async def add_image(file: UploadFile):
    try:
        image_url = await services.add_image(file)
        return {"url": image_url}
    except ImageStorageException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.get("/{image_id}", response_class=FileResponse)
async def get_image(image_id: str):
    matches = fnmatch.filter(os.listdir(IMAGE_DIRECTORY_PATH), image_id + ".*")
    if matches:
        return IMAGE_DIRECTORY_PATH + matches[0]
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"errorCode": ErrorCodes.NONEXISTENT_IMAGE.value})


@app.delete("/{image_id}")
async def delete_image(image_id: str):
    matches = fnmatch.filter(os.listdir(IMAGE_DIRECTORY_PATH), image_id + ".*")
    if not matches:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"errorCode": ErrorCodes.NONEXISTENT_IMAGE.value})
    os.remove(IMAGE_DIRECTORY_PATH + matches[0])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
