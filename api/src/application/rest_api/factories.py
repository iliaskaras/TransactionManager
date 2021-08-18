from fastapi import FastAPI

from application.infrastructure.configurations.models import Configuration
from application.infrastructure.database.database import AsyncMongoDBFactory
from application.infrastructure.error.errors import InvalidArgumentError
from application.infrastructure.loggers.loggers import TransactionManagerAppLoggerFactory
from application.infrastructure.spark.configurations import AppSparkSession
from application.rest_api.transactions import routes as transaction_routes
from application.rest_api.task_status import routes as task_status_route
from application.rest_api.data_ingestion import routes as data_ingestion_route


def create_transaction_manager_app(name: str) -> FastAPI:
    """
    The FastAPI Application Factory for the Transaction Manager application.
    Initializes and returns the Transaction Manager FastAPI application.

    :param name: The name of the FastAPI application.

    @return: The Transaction Manager FastAPI application.
    """
    if not name:
        raise InvalidArgumentError("The application name is required.")

    # Initialize the configuration instance.
    Configuration.initialize()

    # Initialize Application Spark Session.
    AppSparkSession.initialize()

    # Initialize MongoDB.
    AsyncMongoDBFactory.initialize()

    # Initialize the application logger instance.
    TransactionManagerAppLoggerFactory.initialize()
    logger = TransactionManagerAppLoggerFactory.get()

    # Create the FastAPI application.
    rest_api = FastAPI(name=name)

    # Configure the REST API endpoints.
    rest_api.include_router(transaction_routes.router)
    rest_api.include_router(task_status_route.router)
    rest_api.include_router(data_ingestion_route.router)

    logger.info("Transaction Manager REST API started.")

    return rest_api
