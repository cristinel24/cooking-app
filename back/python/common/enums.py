from enum import Enum


class UserRoles(Enum):
    USER = 0b0
    VERIFIED = 0b1
    ADMIN = 0b10
    PREMIUM = 0b100
    BANNED = 0b1000
