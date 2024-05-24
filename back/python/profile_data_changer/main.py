from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from constants import HOST, PORT
from exception import ProfileDataChangerException
import services
import uvicorn
from schemas import UserProfileData

app = FastAPI(title="Profile Data Changer")


@app.patch("/{user_id}", tags=["patch_user, auth"], response_model=None, response_description="Successful operation")
async def patch_user(user_id: str, data: UserProfileData, request: Request) -> None | JSONResponse:
    try:
        # if user_id != request.state.user_id:
        #     raise ProfileDataChangerException(status.HTTP_403_FORBIDDEN, ErrorCodes.UNAUTHORIZED)
        await services.patch_user(user_id, data)
    except ProfileDataChangerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
