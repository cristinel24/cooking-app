from enum import Enum
from fastapi import status
from utils import *

hash_algo_mapping: dict = {
    "argon2": hash_via_argon2,
    "bcrypt": hash_via_bcrypt,
    "random_sha256": hash_via_random_sha256
}


class ErrorCodes(Enum):
    HASHING_FAILED = 20200
    HASH_ALGO_NOT_SUPPORTED = 20201
    HASH_ALGO_NOT_IN_DB = 20202
    DB_CONNECTION_FAILURE = 20203
    FAILED_TO_GET_PRIMARY_HASH_ALGO = 20204
    FAILED_TO_CHECK_HASH_ALGO_EXISTANCE = 20205


ErrorCodesToHTTPCodesMapping: dict[int, int] = {
    ErrorCodes.HASH_ALGO_NOT_IN_DB.value: status.HTTP_405_METHOD_NOT_ALLOWED
}
