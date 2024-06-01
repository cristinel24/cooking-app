import fnmatch
import os.path
from typing import Annotated

from fastapi import FastAPI, UploadFile, status, Header
from fastapi.responses import FileResponse, JSONResponse

import services
from constants import HOST, PORT, IMAGE_DIRECTORY_PATH, ErrorCodes
from exception import ImageStorageException
from schemas import UrlResponse

app = FastAPI(title="Image Storage")


@app.post("/", response_model=UrlResponse, response_description="Successful operation")
async def add_image(file: UploadFile, x_user_id: Annotated[str | None, Header()] = None) -> UrlResponse | JSONResponse:
    if not x_user_id:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"errorCode": ErrorCodes.UNAUTHORIZED_USER.value})
    try:
        image_url = await services.add_image(file)
        return UrlResponse(url=image_url)
    except ImageStorageException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


@app.get("/{image_id}", response_description="Successful operation")
async def get_image(image_id: str):
    matches = fnmatch.filter(os.listdir(IMAGE_DIRECTORY_PATH), image_id + ".*")
    if matches:
        return FileResponse(IMAGE_DIRECTORY_PATH + matches[0])
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"errorCode": ErrorCodes.NONEXISTENT_IMAGE.value})


@app.delete("/{image_id}", response_model=None, response_description="Successful operation")
async def delete_image(image_id: str) -> None | JSONResponse:
    matches = fnmatch.filter(os.listdir(IMAGE_DIRECTORY_PATH), image_id + ".*")
    if not matches:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"errorCode": ErrorCodes.NONEXISTENT_IMAGE.value})
    os.remove(IMAGE_DIRECTORY_PATH + matches[0])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
