from fastapi import FastAPI, status, Response
import uvicorn
import services
import exceptions
from constants import ErrorCodes, HOST, PORT

app = FastAPI()


@app.get("/allergen")
async def get_allergens(response: Response, starting_with: str = ''):
    try:
        return await services.get_allergens_by_starting_string(starting_with)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


@app.post("/allergen/{name}")
async def add_allergen(name: str, response: Response):
    try:
        await services.add_allergen_by_name(name)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


@app.delete("/allergen/{name}")
async def remove_allergen(name: str, response: Response):
    try:
        await services.remove_allergen_by_name(name)
    except exceptions.AllergenException as e:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {"errorCode": e.error_code}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
