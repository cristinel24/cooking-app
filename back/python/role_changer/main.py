from typing import Annotated

import uvicorn
from fastapi import FastAPI, status, Header
from fastapi.responses import JSONResponse

from constants import *
from exceptions import RoleChangerException
from schemas import RoleData
from services import update_user_roles

app = FastAPI(title="Role Changer")


@app.put("/{user_id}/roles", response_model=RoleData, response_description="Successful operation")
async def update_user_roles_route(
        user_id: str, user_roles: RoleData,
        x_user_id: Annotated[str | None, Header()] = None,
        x_user_role: Annotated[int | None, Header()] = None
) -> RoleData | JSONResponse:
    if not x_user_id:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"errorCode": ErrorCodes.UNAUTHORIZED_REQUEST.value})

    if (x_user_role & UserRoles.ADMIN) == 0:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content={"errorCode": ErrorCodes.NONADMIN_REQUEST.value})

    try:
        return update_user_roles(user_id, user_roles)
    except RoleChangerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": ErrorCodes.SERVER_ERROR.value})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
