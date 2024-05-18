from pydantic import BaseModel


class EmailChange(BaseModel):
    email: str
    token: str


class TokenGeneratorRequestResponse(BaseModel):
    value: str
    createdAt: str
    userId: str
    tokenType: str
