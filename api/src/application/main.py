from argparse import ArgumentParser

import uvicorn
from fastapi import FastAPI

from application.rest_api.factories import create_transaction_manager_app

if __name__ == "__main__":
    argument_parser = ArgumentParser(description="Transaction Manager API")

    argument_parser.add_argument(
        "--host",
        dest="host",
        type=str,
        default="127.0.0.1",
    )

    argument_parser.add_argument(
        "--port",
        dest="port",
        type=int,
        default=8000,
    )

    arguments = argument_parser.parse_args()

    transaction_manager_app: FastAPI = create_transaction_manager_app(
        name="Transaction Manager API",
    )

    uvicorn.run(transaction_manager_app, host=arguments.host, port=arguments.port)
