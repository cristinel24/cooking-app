from utils import *

hash_algo_mapping: dict = {
    "argon2": hash_via_argon2,
    "bcrypt": hash_via_bcrypt,
    "random_sha256": hash_via_random_sha256
}
