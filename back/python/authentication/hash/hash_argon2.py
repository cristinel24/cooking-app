from argon2 import PasswordHasher
import secrets
import random


def hash_password(password, salt):
    ph = PasswordHasher()

    hashed_password = ph.hash(password, salt=salt)
    return hashed_password


def generate_salt():
    return secrets.token_bytes(random.randint(8, 8))


if __name__ == "__main__":
    password = "password123"
    salt = generate_salt()
    hashed_password = hash_password(password, salt)
    print("Hashed password:", hashed_password)