from pydantic import BaseModel


class AuthFollowData(BaseModel):
    user_id: str | None = None
    user_roles: int | None = None
    follow_id: str | None = None
