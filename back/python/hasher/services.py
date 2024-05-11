from constants import *
from repository import DBWrapper


def handle_hash_with_primary_algo(target: str, salt: str | None) -> tuple[str, str, str | None]:
    db_wrapper = DBWrapper()
    primary_hash_algorithm_name = db_wrapper.get_primary_hash_algorithm_name()
    hashed_target, generated_salt = handle_hash_with_specific_algo(primary_hash_algorithm_name, target, salt, True)
    return primary_hash_algorithm_name, hashed_target, generated_salt


def handle_hash_with_specific_algo(hash_algorithm_name: str, target: str, salt: str | None, using_primary_algo: bool = False) -> tuple[str, str | None]:
    db_wrapper = DBWrapper()
    if not using_primary_algo and not db_wrapper.check_exists_hash_algorithm_name(hash_algorithm_name):
        raise Exception(ErrorCodes.HASH_ALGO_NOT_IN_DB.value)
    if hash_algorithm_name not in hash_algo_mapping:
        raise Exception(ErrorCodes.HASH_ALGO_NOT_SUPPORTED.value)
    try:
        hashing_result = hash_algo_mapping[hash_algorithm_name](target, salt)
    except Exception:
        raise Exception(ErrorCodes.HASHING_FAILED.value)
    return hashing_result
