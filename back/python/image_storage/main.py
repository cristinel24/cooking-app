import os.path
from io import BytesIO

from fastapi import FastAPI, UploadFile, Response
from fastapi.responses import FileResponse

import services
from constants import HOST_URL, PORT, IMAGE_DIRECTORY_PATH, IMAGE_EXTENSION

app = FastAPI()


@app.put("/")
async def add_image(file: UploadFile):
    return await services.add_image(BytesIO(await file.read()))


@app.get("/{image_id}", response_class=FileResponse)
async def get_image(image_id: str):
    image_path = IMAGE_DIRECTORY_PATH + image_id + IMAGE_EXTENSION
    if os.path.exists(image_path):
        return image_path
    else:
        return Response(status_code=404)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST_URL, port=PORT)
