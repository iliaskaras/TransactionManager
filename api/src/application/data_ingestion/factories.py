from application.infrastructure.loggers.loggers import TransactionManagerAppLoggerFactory
from application.infrastructure.spark.configurations import AppSparkSession
from application.data_ingestion.services import ExcelToMongoDBDataIngestionService


def get_excel_to_mongodb_data_ingestion_service() -> ExcelToMongoDBDataIngestionService:
    return ExcelToMongoDBDataIngestionService(
        spark_session=AppSparkSession.get_instance(),
        logger=TransactionManagerAppLoggerFactory.get()
    )
