import uvicorn
from constants import *
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from exceptions import RoleChangerException
from schemas import RoleData
from services import update_user_roles

app = FastAPI(title="Role Changer")

@app.patch("/{user_id}/roles", response_model=RoleData, response_description="Successful operation")
async def update_user_roles_route(user_id: str, user_roles: RoleData) -> RoleData | JSONResponse:
    try:
        return update_user_roles(user_id, user_roles)
    except RoleChangerException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except Exception:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.SERVER_ERROR.value})

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
