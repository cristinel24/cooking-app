from typing import Annotated
from fastapi import FastAPI, Header, status
from fastapi.responses import JSONResponse
from constants import HOST, PORT, ErrorCodes
from exception import ProfileDataChangerException
import services
import uvicorn
from schemas import UserProfileData

app = FastAPI(title="Profile Data Changer")


@app.patch("/{user_id}", tags=["patch_user, auth"], response_model=None, response_description="Successful operation")
async def patch_user(user_id: str, data: UserProfileData, x_user_id: Annotated[str | None, Header()] = None) -> None | JSONResponse:
    try:
        if user_id != x_user_id:
            raise ProfileDataChangerException(status.HTTP_403_FORBIDDEN, ErrorCodes.UNAUTHORIZED.value)
        await services.patch_user(user_id, data)
    except ProfileDataChangerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,) as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.SERVER_ERROR.value})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
