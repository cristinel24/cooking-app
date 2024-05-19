import uvicorn
from fastapi import FastAPI, status, Response

import exceptions
import services
from constants import ErrorCodes, HOST, PORT

app = FastAPI()


@app.get("/allergen")
async def get_allergens(response: Response, starting_with: str = ''):
    try:
        return await services.get_allergens_by_starting_string(starting_with)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


@app.post("/allergen/{name}/inc")
async def inc_allergen(name: str, response: Response):
    try:
        await services.inc_allergen(name)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


@app.post("/allergens/inc")
async def inc_allergens(names: list[str], response: Response):
    try:
        await services.inc_allergens(names)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


@app.post("/allergen/{name}/dec")
async def dec_allergen(name: str, response: Response):
    try:
        await services.dec_allergen(name)
    except exceptions.AllergenException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"errorCode": e.error_code}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


@app.post("/allergens/dec")
async def dec_allergens(names: list[str], response: Response):
    try:
        await services.dec_allergens(names)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
