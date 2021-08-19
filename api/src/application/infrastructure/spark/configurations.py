from pyspark import SparkConf

from application.infrastructure.configurations.models import Configuration
from pyspark.sql import SparkSession

from application.infrastructure.spark.errors import SparkSessionNotInitializedError


class AppSparkSession:
    INSTANCE: SparkSession = None

    @classmethod
    def initialize(cls) -> None:
        """
        Initializes the SparkSession instance with its Spark Configurations.
        """
        if not cls.INSTANCE:
            configuration: Configuration = Configuration.get_instance()
            spark_conf = SparkConf()
            spark_conf.set('spark.mongodb.input.uri', configuration.spark_input_uri)
            spark_conf.set('spark.mongodb.output.uri', configuration.spark_output_uri)
            spark_conf.set('master', 'local[*]')
            spark_conf.set(
                "spark.jars.packages",
                "com.crealytics:spark-excel_2.12:0.13.8,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1"
            )
            spark_conf.set('spark.driver.memory', configuration.spark_driver_memory)
            spark_conf.setAppName(configuration.spark_app_name)

            cls.INSTANCE: SparkSession = SparkSession.builder.config(conf=spark_conf).getOrCreate()

    @staticmethod
    def get_instance() -> SparkSession:
        """
        Returns the initialized application SparkSession instance.

        :return: The initialized SparkSession instance.

        :raise SparkConfigNotInitializedError: If the SparkConfig has not been initialized.
        """

        if not AppSparkSession.INSTANCE:
            raise SparkSessionNotInitializedError(
                "SparkSession has not been initialized."
            )

        return AppSparkSession.INSTANCE
