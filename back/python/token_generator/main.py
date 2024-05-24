from fastapi.responses import JSONResponse
from schemas import TokenData
import services
from constants import HOST, PORT, Errors
from fastapi import FastAPI, status

app = FastAPI(title="Token Generator")


@app.get("/{user_id}/{token_type}", response_model=TokenData, response_description="Successful operation")
async def get_user_token(user_id: str, token_type: str) -> TokenData | JSONResponse:
    try:
        token = services.insert_user_token(user_id, token_type)
        return TokenData(**token)
    except (services.UserException, services.TokenException) as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"errorCode": Errors.UNKNOWN})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
