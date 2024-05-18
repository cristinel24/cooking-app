from pydantic import BaseModel
from typing import Literal


class AccountVerification(BaseModel):
    email: str
    token: str


class ChangeRequest(BaseModel):
    email: str
    token: str
    changeType: Literal["password", "username", "email"]
