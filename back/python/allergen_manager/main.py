import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

import services
from constants import HOST, PORT, ErrorCodes
from schemas import AllergensBody

app = FastAPI(title="Allergen Manager")


@app.get("/", response_model=AllergensBody, response_description="Successful operation")
async def get_allergens(starting_with: str = '') -> AllergensBody | JSONResponse:
    try:
        allergens = await services.get_allergens_by_starting_string(starting_with)
        return AllergensBody(allergens=allergens)
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": ErrorCodes.SERVER_ERROR.value})


@app.post("/", response_model=None, response_description="Successful operation")
async def update_allergens(action: int, body: AllergensBody) -> None | JSONResponse:
    try:
        match action:
            case 1:
                await services.inc_allergens(body.allergens)
            case -1:
                await services.dec_allergens(body.allergens)
            case _:
                return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                                    content={"errorCode": ErrorCodes.BAD_ACTION.value})
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": ErrorCodes.SERVER_ERROR.value})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
