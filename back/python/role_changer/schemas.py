from pydantic import BaseModel
from typing import Dict

class RoleData(BaseModel):
    roles: Dict[str, int]
