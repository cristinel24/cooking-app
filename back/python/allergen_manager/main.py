import exceptions
from schemas import AllergensBody 
import services
import uvicorn
from constants import HOST, PORT, ErrorCodes
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI(title="Allergen Manager")


@app.get("/allergen", response_model=AllergensBody, response_description="Successful operation")
async def get_allergens(starting_with: str = '') -> AllergensBody | JSONResponse:
    try:
        allergens = await services.get_allergens_by_starting_string(starting_with)
        return AllergensBody(allergens=allergens)
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.SERVER_ERROR.value})


@app.post("/allergen/{name}/inc", response_model=None, response_description="Successful operation")
async def inc_allergen(name: str) -> None | JSONResponse:
    try:
        await services.inc_allergen(name)
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.SERVER_ERROR.value})


@app.post("/allergens/inc", response_model=None, response_description="Successful operation")
async def inc_allergens(body: AllergensBody) -> None | JSONResponse:
    try:
        await services.inc_allergens(body.allergens)
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.SERVER_ERROR.value})


@app.post("/allergen/{name}/dec", response_model=None, response_description="Successful operation")
async def dec_allergen(name: str) -> None | JSONResponse:
    try:
        await services.dec_allergen(name)
    except exceptions.AllergenException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"errorCode": e.error_code})
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.SERVER_ERROR.value})


@app.post("/allergens/dec", response_model=None, response_description="Successful operation")
async def dec_allergens(body: AllergensBody) -> None | JSONResponse:
    try:
        await services.dec_allergens(body.allergens)
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.SERVER_ERROR.value})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
