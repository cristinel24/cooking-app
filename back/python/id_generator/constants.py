from enum import Enum, unique

ID_PROJECTION = {"_id": 0, "value": 1}
MAX_TIMEOUT_TIME_SECONDS = 3  # 3 seconds timeout

@unique
class ErrorCode(Enum):
    DB_ERROR_ID_GENERATOR = 20301  # Failed to fetch or update the ID
    DB_ERROR_ACCESS = 20302  # Error accessing database

