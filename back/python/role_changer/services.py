from constants import ErrorCodes, UserRoles
from exceptions import RoleChangerException
from fastapi import status
from repository import MongoCollection
from schemas import *

user_collection = MongoCollection()


def update_user_roles(user_id: str, role_data: RoleData):
    roles = user_collection.get_user_roles(user_id)

    for role, value in role_data.__dict__.items():
        if value == 0:
            continue

        if not hasattr(UserRoles, role.upper()):
            raise RoleChangerException(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCodes.NONEXISTENT_ROLES.value,
            )

        role_bit = getattr(UserRoles, role.upper())

        if value > 0:
            roles |= role_bit
        else:
            roles &= ~role_bit

    user_collection.update_roles(user_id, roles)
    return RoleData(
        verified=roles & UserRoles.VERIFIED > 0,
        admin=roles & UserRoles.ADMIN > 0,
        premium=roles & UserRoles.PREMIUM > 0,
        banned=roles & UserRoles.BANNED > 0,
    )
