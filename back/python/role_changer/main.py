from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
import uvicorn
from dotenv import load_dotenv
from schemas import RoleData
from services import update_user_roles_logic
from constants import *

load_dotenv()

app = FastAPI(title="Role Changer")

@app.patch("/admin/users/{user_id}/roles", response_model = RoleData, response_description="Successful operation")
async def update_user_roles(user_id: str, user_roles: RoleData) -> RoleData | JSONResponse:
    try:
        res = update_user_roles_logic(user_id, user_roles)
        if res != 0:
            if res == ErrorCodes.NONEXISTENT_ROLES:
                return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTED, content={"errorCode": ErrorCodes.SERVER_ERROR.value})
            elif res == ErrorCodes.NONEXISTENT_USER:
                 return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"errorCode": ErrorCodes.SERVER_ERROR.value})
            return JSONResponse(content={"errorCode": res.value})
        print(user_roles.roles)
        return RoleData(roles=user_roles.roles)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": ErrorCodes.SERVER_ERROR.value})

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
