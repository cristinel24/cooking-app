from argon2 import PasswordHasher
import secrets


ALGORITHM = "argon2"


def hash_password(hashing_password, hashing_salt):
    ph = PasswordHasher()

    hashed_password = ph.hash(hashing_password, salt=hashing_salt)
    return hashed_password


def generate_salt():
    return secrets.token_bytes(32)


# if __name__ == "__main__":
#     password = "password123"
#     salt = generate_salt()
#     pw = hash_password(password, salt)
#     print("Hashed password:", pw)
