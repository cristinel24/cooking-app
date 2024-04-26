from fastapi import FastAPI, APIRouter

app = FastAPI()

router = APIRouter(
    prefix="/api/users"
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

