from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
import uvicorn
from constants import HOST, PORT, ErrorCodesToHTTPCodesMapping
from schemas import HashData, PrimaryHashData
from services import handle_hash_with_primary_algo, handle_hash_with_specific_algo

app = FastAPI(title="Hasher")


@app.get("/{target}", response_model=PrimaryHashData, response_description="Successful operation")
async def hash_with_primary_algo(target: str, salt: str | None = None) -> PrimaryHashData | JSONResponse:
    try:
        hash_algorithm_name, hashed_target, generated_salt = handle_hash_with_primary_algo(target, salt)
        return PrimaryHashData(hashAlgorithmName=hash_algorithm_name, hash=hashed_target, salt=generated_salt)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_code = int(str(e))
        if error_code in ErrorCodesToHTTPCodesMapping:
            status_code = ErrorCodesToHTTPCodesMapping[error_code]
        return JSONResponse(status_code=status_code, content={"errorCode": error_code})


@app.get("/{hash_algorithm_name}/{target}", response_model=HashData, response_description="Successful operation")
async def hash_with_specific_algo(hash_algorithm_name: str, target: str, salt: str | None = None) -> HashData | JSONResponse:
    try:
        hashed_target, generated_salt = handle_hash_with_specific_algo(hash_algorithm_name, target, salt)
        return HashData(hash=hashed_target, salt=generated_salt)
    except Exception as e:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_code = int(str(e))
        if error_code in ErrorCodesToHTTPCodesMapping:
            status_code = ErrorCodesToHTTPCodesMapping[error_code]
        return JSONResponse(status_code=status_code, content={"errorCode": error_code})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
