import os

from celery import Celery

from application.infrastructure.configurations.models import Configuration
from application.infrastructure.spark.configurations import AppSparkSession

# Initialize the configuration instance.
Configuration.initialize()

# Initialize Application Spark Session.
AppSparkSession.initialize()

# Initialize Celery.
celery = Celery(
    'Transaction Manager API',
    # Register tasks.
    include=[
        'application.data_ingestion.tasks',
        'application.transactions.tasks',
    ],
)

celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


