import argon2
import bcrypt
import secrets


def hash_via_argon2(target: str, salt: str | None) -> tuple[str, str | None]:
    if salt is None:
        salt_to_use = secrets.token_hex(12)
        output_salt = salt_to_use
    else:
        salt_to_use = salt
        output_salt = None

    hashed_target = argon2.PasswordHasher().hash(target, salt=salt_to_use.encode('utf-8'))
    return hashed_target, output_salt


def hash_via_bcrypt(target: str, salt: str | None) -> tuple[str, str | None]:
    if salt is None:
        salt_to_use = bcrypt.gensalt().decode('utf-8')
        output_salt = salt_to_use
    else:
        salt_to_use = salt
        output_salt = None

    hashed_target = bcrypt.hashpw(target.encode("utf8"), salt_to_use.encode("utf8")).decode("utf-8")
    return hashed_target, output_salt


def hash_via_random_sha256(target: str, salt: str | None) -> tuple[str, str | None]:
    output_salt = "" if salt is None else None
    return target, output_salt
