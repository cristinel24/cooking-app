from typing import Optional, Annotated

from starlette.responses import JSONResponse

import services
import uvicorn
from fastapi import FastAPI, status, Query, Header

from report_manager.constants import HOST, PORT, ErrorCodes
from report_manager.exception import ReportManagerException
from report_manager.schemas import ReportsResponse, ReportCreateData
from report_manager.utils import build_response_from_values

app = FastAPI(title="Report manager")


@app.get("/", response_model=ReportsResponse, response_description="Successful operation")
async def get_reports(
        start: int = Query(0, ge=0),
        count: int = Query(10, ge=1),
        filter: Optional[str] = None,
        sort: Optional[str] = None,
        x_user_id: Annotated[str | None, Header()] = None
) -> ReportsResponse | JSONResponse:
    if not x_user_id:
        return build_response_from_values(status.HTTP_401_UNAUTHORIZED, ErrorCodes.UNAUTHENTICATED.value)
    try:
        result = await services.get_reports_by_type(reported_type=filter, skip=start, limit=count)
        return result
    except ReportManagerException as e:
        return build_response_from_values(status_code=e.status_code, error_code=e.error_code)


@app.post("/", response_model=None, response_description="Successful operation")
async def create_report(
        report_data: ReportCreateData,
        x_user_id: Annotated[str | None, Header()] = None,
        x_user_roles: Annotated[str | None, Header()] = None
) -> JSONResponse | None:
    if not x_user_id:
        return build_response_from_values(status.HTTP_401_UNAUTHORIZED, ErrorCodes.UNAUTHENTICATED.value)
    if x_user_roles and "admin" not in x_user_roles:
        return build_response_from_values(status.HTTP_403_FORBIDDEN, ErrorCodes.UNAUTHORIZED.value)
    try:
        services.create_report(report_data)
    except ReportManagerException as e:
        return build_response_from_values(status_code=e.status_code, error_code=e.error_code)


@app.patch("/{report_id}", response_model=None, response_description="Successful operation")
async def update_report(solverId: str, report_id,
                        x_user_id: Annotated[str | None, Header()] = None,
                        x_user_roles: Annotated[str | None, Header()] = None) -> JSONResponse | None:
    if not x_user_id:
        return build_response_from_values(status.HTTP_401_UNAUTHORIZED, ErrorCodes.UNAUTHENTICATED.value)
    if x_user_roles and "admin" not in x_user_roles:
        return build_response_from_values(status.HTTP_403_FORBIDDEN, ErrorCodes.UNAUTHORIZED.value)
    try:
        services.update_report(solverId, report_id)
    except ReportManagerException as e:
        return build_response_from_values(status_code=e.status_code, error_code=e.error_code)


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
