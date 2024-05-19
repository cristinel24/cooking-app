from repository import MongoCollection
from schemas import *

def update_roles_in_db(user_id: str, roles: Dict[str, int]):
    db = MongoCollection()
    return db.update_roles(user_id, roles)

def update_user_roles_logic(user_id: str, role_data: RoleData):
    return update_roles_in_db(user_id, role_data.roles)
