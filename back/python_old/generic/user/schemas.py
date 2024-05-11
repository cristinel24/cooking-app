from pydantic import BaseModel


class AccountChangeData(BaseModel):
    display_name: str | None = None
    icon: str | None = None
    description: str | None = None
    allergens: list[str] | None = None
