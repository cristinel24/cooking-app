from pydantic import BaseModel


class AccountChangeData(BaseModel):
    display_name: str | None
    icon: str | None
    description: str | None
    allergens: list[str] | None
