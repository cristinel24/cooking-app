from pydantic import BaseModel


class NewUserData(BaseModel):
    username: str
    email: str
    password: str
    displayName: str = None
