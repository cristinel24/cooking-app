from pydantic import BaseModel
from typing import Literal


class CredentialChangeRequest(BaseModel):
    email: str
    changeType: Literal["password", "username", "email"]


class ChangeRequest(BaseModel):
    email: str
    token: str
    changeType: Literal["password", "username", "email"]
