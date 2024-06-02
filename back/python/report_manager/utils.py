from starlette.responses import JSONResponse

from report_manager.exception import ReportManagerException


def build_response_from_exception(exception: ReportManagerException) -> JSONResponse:
    return build_response_from_values(exception.status_code, exception.error_code)


def build_response_from_values(status_code: int, error_code: int) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"errorCode": error_code})
