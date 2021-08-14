import uvicorn
from fastapi import FastAPI

from application.rest_api.factories import create_transaction_manager_app

application: FastAPI = create_transaction_manager_app(
    name="Transaction Manager API",
)

if __name__ == "__main__":

    uvicorn.run(application, host="127.0.0.1", port=8000)
