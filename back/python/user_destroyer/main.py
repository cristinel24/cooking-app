import json

from fastapi import FastAPI, Response

import services
from constants import HOST, PORT
from exception import UserDestroyerException

app = FastAPI()


@app.delete("/user/{user_id}", tags=["user-destroyer"])
async def delete_user(user_id: str):
    try:
        return await services.delete_user(user_id)
    except UserDestroyerException as e:
        return Response(status_code=e.status_code, content=json.dumps({"errorCode": e.error_code.value}))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
