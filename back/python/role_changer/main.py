from fastapi import FastAPI, status
import uvicorn
from dotenv import load_dotenv
from schemas import *
from repository import *
from services import *

load_dotenv()

app = FastAPI()

@app.patch("/admin/users/{user_id}/roles")
async def update_user_roles(user_id: str, user_roles: RoleData):
    try:
        res = update_user_roles_logic(user_id, user_roles)
        if res == 0:
            return { "msg" : "Roles added succesfully" }
        return { "errorCode" : res }
    except (Exception,) as e:
        return { "errorCode": ErrorCodes.SERVER_ERROR.value }
if __name__ == "__main__":
   uvicorn.run(app, host=os.getenv("HOST", "localhost"), port=int(os.getenv("PORT", 8000)))
