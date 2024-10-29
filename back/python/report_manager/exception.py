from constants import ErrorCodes


class ReportManagerException(Exception):

    def __init__(self, error_code: ErrorCodes | int, status_code: int):

        if isinstance(error_code, ErrorCodes):
            self.error_code = error_code.value
        else:
            self.error_code = error_code

        self.status_code = status_code

    def __repr__(self):
        return f"ReportManagerException(error_code={self.error_code}, status_code={self.status_code})"

    def __str__(self):
        return repr(self)
