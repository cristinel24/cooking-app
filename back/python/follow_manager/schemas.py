from pydantic import BaseModel


class AuthFollowData(BaseModel):
    user_id: str
    user_roles: int
    follow_id: str
