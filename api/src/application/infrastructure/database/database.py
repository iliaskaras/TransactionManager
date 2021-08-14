import motor
from motor.motor_asyncio import AsyncIOMotorClient
import motor.motor_asyncio

from application.infrastructure.configurations.models import Configuration


class AsyncMongoDBFactory:

    DATABASE = None

    @classmethod
    def initialize(cls) -> None:
        """
        Creates an asyncio mongodb client and initializes the global application mongodb.
        If the database do not exist, it will be created.
        """
        client: AsyncIOMotorClient = motor.motor_asyncio.AsyncIOMotorClient(
            Configuration.get_instance().mongodb_connection_uri
        )
        # client.transactions will create mongodb transactions at the provided mongodb connection uri
        # if the database don't exist.
        cls.DATABASE = client.transactions

    @classmethod
    def get(cls):
        if not cls.DATABASE:
            cls.initialize()

        return cls.DATABASE
