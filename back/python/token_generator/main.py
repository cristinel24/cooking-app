import services
from constants import HOST, PORT
from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/{user_id}/{token_type}")
async def get_user_token(user_id: str, token_type: str, response: Response) -> dict:
    try:
        token = services.insert_user_token(user_id, token_type)
        print(token)
        return token
    except services.UserException as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code}
    except services.TokenException as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
