from fastapi import FastAPI, Response
from constants import HOST_URL, PORT
from exception import ProfileDataChangerException
import services
import uvicorn
from schemas import UserProfileData
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()


@app.patch("/{user_id}")
async def patch_user(user_id: str, user_roles: int, data: UserProfileData, response: Response) -> None | dict:
    try:
        return await services.patch_user(user_id, data)
    except ProfileDataChangerException as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST_URL, port=PORT)
