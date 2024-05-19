import services
from constants import HOST, PORT, Errors
from fastapi import FastAPI, Response, status

app = FastAPI()


@app.get("/{user_id}/{token_type}")
async def get_user_token(user_id: str, token_type: str, response: Response) -> dict:
    try:
        token = services.insert_user_token(user_id, token_type)
        return token
    except (services.UserException, services.TokenException) as e:
        response.status_code = e.status_code
        return {"errorCode": e.error_code}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": Errors.UNKNOWN}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
