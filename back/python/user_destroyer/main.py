from fastapi import FastAPI
from fastapi.responses import JSONResponse

import services
from constants import HOST, PORT
from exception import UserDestroyerException

app = FastAPI(title="User Destroyer")


@app.delete("/{user_id}", tags=["user-destroyer"], response_model=None, response_description="Successful operation")
async def delete_user(user_id: str) -> None | JSONResponse:
    try:
        await services.delete_user(user_id)
    except UserDestroyerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code.value})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
