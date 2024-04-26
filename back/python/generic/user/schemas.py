from pydantic import BaseModel


# to be tested
class AccountChangeData(BaseModel):
    display_name: str | None
    icon: str | None
    description: str | None
    allergens: list[str] | None



