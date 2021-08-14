from fastapi import FastAPI

from application.infrastructure.configurations.models import Configuration
from application.infrastructure.database.database import AsyncMongoDBFactory
from application.infrastructure.error.errors import InvalidArgumentError
from application.infrastructure.loggers.loggers import TransactionManagerAppLoggerFactory
from application.rest_api.health_check import routes as health_check_route
from application.rest_api.students import routes as students_route


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
    configuration = Configuration.initialize()

    # Initialize MongoDB.
    AsyncMongoDBFactory.initialize()

    # Initialize the application logger instance.
    TransactionManagerAppLoggerFactory.initialize()
    logger = TransactionManagerAppLoggerFactory.get()

    # Create the FastAPI application.
    rest_api = FastAPI(name=name)

    # Configure the REST API endpoints.
    rest_api.include_router(health_check_route.router)
    rest_api.include_router(students_route.router)

    logger.info("Transaction Manager REST API started.")

    return rest_api
