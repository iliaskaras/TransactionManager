import os

from celery import Celery

from application.infrastructure.configurations.models import Configuration
from application.infrastructure.spark.configurations import AppSparkSession

# Initialize the configuration instance.
Configuration.initialize()

# Initialize Application Spark Session.
AppSparkSession.initialize()

celery = Celery(
    'Transaction Manager API',
    include=['application.rest_api.data_ingestion.tasks'],
)

celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


