import os
from pymongo import MongoClient, errors, timeout
from constants import *
from schemas import *

class MongoCollection:
    def __init__(self, connection: MongoClient | None = None):
        if connection is not None:
            self._connection = connection
        else:
            self._connection = MongoClient(MONGO_URI)
        self._collection = self._connection[DB_NAME]['user']

    def update_roles(self, user_id: str, roles: RoleData) -> None:
        with timeout(MAX_TIMEOUT_TIME_SECONDS):
            try:
                user = self._collection.find_one({"id": user_id})
                if not user:
                    return ErrorCodes.NONEXISTENT_USER

                current_roles = user.get("roles", UserRoles.ACTIVE)
                new_roles = current_roles

                for role, value in roles.items():
                    if not hasattr(UserRoles, role.upper()):
                        return ErrorCodes.NONEXISTENT_ROLES

                    role_bit = getattr(UserRoles, role.upper())
                    
                    if value == 1:
                        new_roles |= role_bit  
                    elif value == -1:
                        new_roles &= ~role_bit  
                    else:
                        return ErrorCodes.NONEXISTENT_ROLES

                if new_roles & UserRoles.BANNED:
                    result = self._collection.update_one(
                        {"id": user_id},
                        {"$bit": {"roles": {"or": new_roles}}}
                    )
                else:
                    result = self._collection.update_one(
                        {"id": user_id},
                        {"$set": {"roles": new_roles}}
                    )

                if result.matched_count == 0:
                    return ErrorCodes.NONEXISTENT_USER

                return 0
            except errors.PyMongoError as e:
                return ErrorCodes.FAILED_ROLES
