from typing import Annotated

from fastapi import FastAPI, Response, status, Header
from constants import HOST, PORT, ErrorCodes
from exception import ProfileDataChangerException
import services
import uvicorn
from schemas import UserProfileData

app = FastAPI()


@app.patch("/{user_id}", tags=["patch_user, auth"])
async def patch_user(user_id: str, data: UserProfileData, response: Response,
                     x_user_id: Annotated[str | None, Header()] = None) -> None | dict:
    try:
        if user_id != x_user_id:
            raise ProfileDataChangerException(status.HTTP_403_FORBIDDEN, ErrorCodes.NOT_AUTHENTICATED.value)
        return await services.patch_user(user_id, data)
    except ProfileDataChangerException as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code}
    except (Exception,):
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
