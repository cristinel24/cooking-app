from repository import ReportCollection
from schemas import *
from api import *

report_collection = ReportCollection()


def get_reports_by_type(reported_type: str, skip: int, limit: int) -> ReportsResponse:
    try:
        valid_filters = ["rating", "recipe", "user"]
        reported_type.removesuffix("s")
        if reported_type not in valid_filters:
            reports = report_collection.get_reports(skip, limit)
        else:
            reports = report_collection.get_reports_by_type(reported_type, skip, limit)

        report_cards = []
        for report in reports["data"]:
            author_data = get_user_card(report["authorId"])
            if report["reportedType"] == "rating":
                reported_data = get_rating_data_card(report["reportedId"])
            elif report["reportedType"] == "recipe":
                reported_data = get_recipe_data(report["reportedId"])
            elif report["reportedType"] == "user":
                reported_data = get_user_data(report["reportedId"])

            report_card = (
                report["_id"],
                author_data,
                report["reportedType"],
                reported_data,
                report["createdAt"]
            )

            report_cards.append(report_card)
        return ReportsResponse(data=report_cards, total=reports["total"])
    except ReportManagerException as e:
        raise e


def create_report(report_data: ReportCreateData) -> None:
    if report_data.reportedType not in ["rating", "recipe", "user"]:
        raise ReportManagerException(status.HTTP_406_NOT_ACCEPTABLE, ErrorCodes.INVALID_REPORT_TYPE.value)
    report_collection.create_report(report_data)


def update_report(solverId: str, report_id: str) -> None:
    report_collection.update_report(solverId, report_id)
