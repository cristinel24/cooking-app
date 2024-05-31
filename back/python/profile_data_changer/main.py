from typing import Annotated
from fastapi import FastAPI, Header, status
from fastapi.responses import JSONResponse
from constants import HOST, PORT, ErrorCodes, UserRoles
from exception import ProfileDataChangerException
import services
import uvicorn
from schemas import UserProfileData

app = FastAPI(title="Profile Data Changer")


@app.patch("/{user_id}", tags=["patch_user, auth"], response_model=None, response_description="Successful operation")
async def patch_user(
        user_id: str, data: UserProfileData,
        x_user_id: Annotated[str | None, Header()] = None,
        x_user_roles: Annotated[str | None, Header()] = None
) -> None | JSONResponse:
    if not x_user_id:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"errorCode": ErrorCodes.UNAUTHORIZED_REQUEST.value})

    try:
        user_roles = int(x_user_roles)
    except ValueError:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"errorCode": ErrorCodes.USER_ROLES_INVALID_VALUE.value})

    if user_id != x_user_id and not user_roles & UserRoles.ADMIN:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content={"errorCode": ErrorCodes.FORBIDDEN_REQUEST.value})

    try:
        await services.patch_user(user_id, data)
    except ProfileDataChangerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": ErrorCodes.SERVER_ERROR.value})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
