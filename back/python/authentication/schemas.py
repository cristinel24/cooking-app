from pydantic import BaseModel
from typing import Optional


class RegisterData(BaseModel):
    username: str
    display_name: Optional[str]
    email: str
    password: str


class LoginData(BaseModel):
    identifier: str
    password: str


class AccountChangeData(BaseModel):
    type: str
    email: str


class ConfirmAccountChangeData(BaseModel):
    token: str
    changedField: str
