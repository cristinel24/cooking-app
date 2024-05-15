from pydantic import BaseModel


WAIT_ON_ERROR = 5


class LoginData(BaseModel):
    identifier: str
    password: str
