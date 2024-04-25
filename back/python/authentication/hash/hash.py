from authentication.hash import hash_argon2


HASH_ALGORITHM = "argon2"


def hash_password(password):
    salt = hash_argon2.generate_salt()
    password_hash = hash_argon2.hash_password(password, salt)

    return {
        "hash": password_hash,
        "salt": salt
    }