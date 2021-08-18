from application.infrastructure.spark.configurations import AppSparkSession
from application.rest_api.data_ingestion.services import ExcelToMongoDBDataIngestionService


def get_excel_to_mongodb_data_ingestion_service() -> ExcelToMongoDBDataIngestionService:
    return ExcelToMongoDBDataIngestionService(
        spark_session=AppSparkSession.get_instance()
    )
