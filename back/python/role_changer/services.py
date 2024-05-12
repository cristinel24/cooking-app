from repository import *
from schemas import *

def update_roles_in_db(user_id: str, roles: int):
    db = MongoCollection()
    return db.update_roles(user_id, roles)


def update_user_roles_logic(user_id: str, role_data: RoleData):
    current_roles = role_data.roles
    
    if current_roles ^ UserRoles.BANNED == 0:  
        new_roles = UserRoles.BANNED  

    else:
        new_roles = current_roles 

    return update_roles_in_db(user_id, new_roles)
    
     
