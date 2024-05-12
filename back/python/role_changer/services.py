from repository import *
from schemas import *

def update_roles_in_db(user_id: str, roles: int):
    db = MongoCollection()
    return db.update_roles(user_id, roles)


def update_user_roles_logic(user_id: str, role_data: RoleData):
    new_roles = role_data.roles 
    return update_roles_in_db(user_id, new_roles)
    
     
