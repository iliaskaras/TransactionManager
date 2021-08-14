from fastapi import FastAPI

from application.infrastructure.configurations.models import Configuration
from application.infrastructure.error.errors import InvalidArgumentError
from application.infrastructure.loggers.loggers import TransactionManagerAppLoggerFactory


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

    # Initialize the application logger instance.
    TransactionManagerAppLoggerFactory.initialize()
    logger = TransactionManagerAppLoggerFactory.get()

    # Create the FastAPI application.
    rest_api = FastAPI(name=name)

    logger.info("Transaction Manager REST API started.")

    return rest_api
