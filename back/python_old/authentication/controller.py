from fastapi import APIRouter

from authentication import schemas, services

router = APIRouter(
    prefix="/api/auth"
)


@router.post("/register")
async def register(data: schemas.RegisterData):
    response = services.register(data)
    return response


@router.post("/verify")
async def verify(token: str):
    response = services.verify(token)
    return response


@router.post("/login")
async def login(data: schemas.LoginData):
    response = services.login(data)
    return response


@router.post("/request_change")
async def request_change(data: schemas.AccountChangeData):
    return {}


@router.post("/confirm_change")
async def confirm_change(data: schemas.ConfirmAccountChangeData):
    return {}


@router.get("/is_authenticated/{token}")
async def is_authenticated(token):
    return services.is_authenticated(token)
