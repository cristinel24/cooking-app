from typing import Optional, Any

import pymongo
from bson import ObjectId
from fastapi import status
from pymongo import MongoClient, errors
from constants import DB_NAME, MONGO_TIMEOUT, MONGO_URI, ErrorCodes
from exception import ReportManagerException
from schemas import ReportCreateData


class MongoCollection:
    def __init__(self, connection: Optional[MongoClient] = None):
        self._connection = connection if connection is not None else MongoClient(MONGO_URI)


class ReportCollection(MongoCollection):
    def __init__(self, connection: Optional[MongoClient] = None):
        super().__init__(connection)
        db = self._connection.get_database(DB_NAME)
        self.collection = db.report

    def get_reports_by_type(self, reported_type: str, skip: int = 0, limit: int = 10) -> dict[str, list[Any] | Any]:
        try:
            with pymongo.timeout(MONGO_TIMEOUT):
                filter_query = {"reportedType": reported_type} if reported_type else {}
                cursor = self.collection.find(filter_query).sort("_id", pymongo.ASCENDING).skip(skip).limit(limit)

                reports = []
                for report in cursor:
                    report_id = ObjectId(report["_id"])
                    report["createdAt"] = report_id.generation_time
                    report.pop("_id")
                    reports.append(report)

                total_count = self.collection.count_documents(filter_query)
                return {
                    "data": reports,
                    "total": total_count
                }
        except errors.PyMongoError as e:
            if e.timeout:
                raise ReportManagerException(status.HTTP_504_GATEWAY_TIMEOUT, ErrorCodes.DATABASE_TIMEOUT.value)
            else:
                raise ReportManagerException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.DATABASE_ERROR.value)

    def get_reports(self, skip: int = 0, limit: int = 10) -> dict[str, list[Any] | Any]:
        try:
            with pymongo.timeout(MONGO_TIMEOUT):
                cursor = self.collection.find().sort("_id", pymongo.ASCENDING).skip(skip).limit(limit)

                reports = []
                for report in cursor:
                    report_id = ObjectId(report["_id"])
                    report["createdAt"] = report_id.generation_time
                    report.pop("_id")
                    reports.append(report)

                return {
                    "data": reports,
                    "total": cursor.count()
                }
        except errors.PyMongoError as e:
            if e.timeout:
                raise ReportManagerException(status.HTTP_504_GATEWAY_TIMEOUT, ErrorCodes.DATABASE_TIMEOUT.value)
            else:
                raise ReportManagerException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.DATABASE_ERROR.value)

    def create_report(self, report_data: ReportCreateData) -> None:
        try:
            with pymongo.timeout(MONGO_TIMEOUT):
                updated_count = self.collection.insert_one(report_data)
                if updated_count.inserted_id is None:
                    raise ReportManagerException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.DATABASE_ERROR.value)
        except errors.PyMongoError as e:
            if e.timeout:
                raise ReportManagerException(status.HTTP_504_GATEWAY_TIMEOUT, ErrorCodes.DATABASE_TIMEOUT.value)

    def update_report(self, solverId: str, report_id: str) -> None:
        try:
            with pymongo.timeout(MONGO_TIMEOUT):
                updated_count = self.collection.update_one({"id": report_id}, {"$set": {"solverId": solverId}})
                if updated_count.modified_count == 0:
                    raise ReportManagerException(status.HTTP_404_NOT_FOUND, ErrorCodes.REPORT_NOT_FOUND.value)
        except errors.PyMongoError as e:
            if e.timeout:
                raise ReportManagerException(status.HTTP_504_GATEWAY_TIMEOUT, ErrorCodes.DATABASE_TIMEOUT.value)
            else:
                raise ReportManagerException(status.HTTP_500_INTERNAL_SERVER_ERROR, ErrorCodes.DATABASE_ERROR.value)
        pass
