from enum import Enum, unique

ID_PROJECTION = {"_id": 0, "value": 1}

@unique
class ErrorCode(Enum):
    ERROR_20301 = 20301  # Failed to fetch or update the ID
    MAX_TIMEOUT_TIME_SECONDS = 3  # 3 seconds timeout
