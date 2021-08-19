from typing import Optional

from pyspark.sql import SparkSession

from application.data_ingestion.errors import ExcelFileLoadingError, MongoDBDataWriteError
from application.infrastructure.error.errors import NoneArgumentError
from application.transactions.schemas import schema
from logging import Logger


class ExcelToMongoDBDataIngestionService:

    def __init__(
            self,
            spark_session: SparkSession,
            logger: Logger
    ):
        self.spark_session: SparkSession = spark_session
        self.logger: Logger = logger

    def apply(self, filepath: str, excel_sheet_name: Optional[str]) -> str:
        """
        Loads an excel file using the global spark session and loads it into the MongoDB database.

        :param filepath: The excel filepath to load.
        :param excel_sheet_name: The excel sheet name.

        :raises: NoneArgumentError: If the filepath is not provided.
        """
        if not filepath:
            raise NoneArgumentError("Filepath is not provided.")

        try:
            df = self.spark_session.read.format("com.crealytics.spark.excel") \
                .option("useHeader", "true") \
                .option("header", "true") \
                .option("inferSchema", "true") \
                .option("dataAddress", excel_sheet_name) \
                .schema(schema) \
                .load(filepath)
        except Exception:
            raise ExcelFileLoadingError("Failed to load the excel file {0}")

        try:
            df.write.format("mongo").mode("append").save()
        except Exception:
            raise MongoDBDataWriteError("Failed to write data to the database")

        return "Data from '{0}' ingested into MongoDB successfully.".format(filepath)
