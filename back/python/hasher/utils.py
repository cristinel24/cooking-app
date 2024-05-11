import argon2
import bcrypt


def hash_via_argon2(target: str) -> str:
    return argon2.PasswordHasher().hash(target)


def hash_via_bcrypt(target: str) -> str:
    return bcrypt.hashpw(target.encode("utf8"), bcrypt.gensalt()).decode("utf-8")


def hash_via_random_sha256(target: str) -> str:
    return target
