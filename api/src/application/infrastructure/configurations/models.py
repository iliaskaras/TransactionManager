import os

from application.infrastructure.configurations.enums import APIEnvironment
from application.infrastructure.configurations.errors import (
    ConfigurationNotInitializedError,
)
from application.infrastructure.error.errors import InvalidArgumentError

API_ENVIRONMENT = "TRANSACTION_MANAGER_API_ENVIRONMENT"


class Configuration:
    """
    The Application Configuration which is initialized at the application start up. Is singleton and is being
    used during the whole application lifecycle.
    """
    INSTANCE: "Configuration" = None

    def __init__(
            self,
            mongodb_connection_uri: str,
            celery_broker_url: str,
            celery_result_backend: str,
            debug: bool = False,
    ):
        if not mongodb_connection_uri:
            raise InvalidArgumentError("The MongoDB connection uri is required.")
        if not celery_broker_url:
            raise InvalidArgumentError("The Celery Broker url is required.")
        if not celery_result_backend:
            raise InvalidArgumentError("The Celery Result backend is required.")
        if not isinstance(debug, bool):
            raise InvalidArgumentError("The Debug flag is not a boolean.")

        self.mongodb_connection_uri = mongodb_connection_uri
        self.celery_broker_url = celery_broker_url
        self.celery_result_backend = celery_result_backend
        self.debug = debug

    @classmethod
    def initialize(cls) -> "Configuration":
        """
        Initializes the Configuration.

        :return The Configuration instance.
        """
        environment: str = os.getenv(API_ENVIRONMENT, None)
        if environment not in APIEnvironment.values():
            raise InvalidArgumentError(
                'Not supported api environment {0}, Choose a supported application environment, available: {1}'.format(
                    API_ENVIRONMENT, APIEnvironment.values()
                )
            )

        if environment == APIEnvironment.local:
            Configuration.INSTANCE = Configuration._initialize_local_configuration()
        elif environment == APIEnvironment.test:
            Configuration.INSTANCE = Configuration._initialize_test_configuration()

        return Configuration.INSTANCE

    @staticmethod
    def get_instance() -> "Configuration":
        """
        Returns the already initialized application configuration instance.

        :return: The initialized configuration instance.

        :raise ConfigurationNotInitializedError: If the configuration has not been initialized.
        """

        if not Configuration.INSTANCE:
            raise ConfigurationNotInitializedError(
                "Configuration has not been initialized."
            )

        return Configuration.INSTANCE

    @staticmethod
    def _initialize_local_configuration() -> "Configuration":
        """
        Initializes and returns a local configuration instance.

        :return: The local configuration instance.
        """
        return Configuration(
            mongodb_connection_uri=os.getenv("MONGODB_CONNECTION_URI"),
            celery_broker_url=os.getenv("CELERY_BROKER_URL"),
            celery_result_backend=os.getenv("CELERY_RESULT_BACKEND"),
            debug=True,
        )

    @staticmethod
    def _initialize_test_configuration() -> "Configuration":
        """
        Initializes and returns a test configuration instance.

        :return: The test configuration instance.
        """
        return Configuration(
            mongodb_connection_uri='',
            celery_broker_url="redis://localhost:6379",
            celery_result_backend="redis://localhost:6379",
            debug=True,
        )
