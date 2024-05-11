from io import BytesIO

from fastapi import FastAPI, UploadFile

import services
from constants import HOST_URL, PORT

app = FastAPI()


@app.put("/")
async def add_image(file: UploadFile):
    return await services.add_image(BytesIO(await file.read()))


@app.get("/{image_id}")
async def get_image(image_id: str):
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST_URL, port=PORT)
