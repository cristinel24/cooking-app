from pydantic import BaseModel


class RoleData(BaseModel):
    verified: int = 0
    admin: int = 0
    premium: int = 0
    banned: int = 0
