from pyspark.sql import SparkSession

from application.infrastructure.spark.configurations import AppSparkSession


class BaseSparkRepository:
    """
    Base Spark Repository class.
    """
    def __init__(self):
        self.spark_session: SparkSession = AppSparkSession.get_instance()
