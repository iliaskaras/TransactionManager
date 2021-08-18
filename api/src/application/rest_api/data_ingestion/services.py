from typing import Optional

from pyspark.sql import SparkSession

from application.infrastructure.error.errors import NoneArgumentError


class ExcelToMongoDBDataIngestionService:

    def __init__(self, spark_session: SparkSession):
        self.spark_session: SparkSession = spark_session

    def apply(self, filepath: str, data_address: Optional[str]):
        if not filepath:
            raise NoneArgumentError("Filepath is not provided.")

        df = self.spark_session.read.format("com.crealytics.spark.excel") \
            .option("useHeader", "true") \
            .option("header", "true") \
            .option("inferSchema", "true") \
            .option("dataAddress", data_address) \
            .load(filepath)

        df.write.format("mongo").mode("append").save()

        return "Data from '{0}' ingested into mongodb successfully.".format(filepath)
