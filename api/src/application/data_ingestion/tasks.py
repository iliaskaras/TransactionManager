from typing import Union, Optional

from celery import states, Task

from application.celery_worker import celery
from application.data_ingestion.factories import get_excel_to_mongodb_data_ingestion_service
from application.infrastructure.loggers.loggers import TransactionManagerAppLoggerFactory
from application.tasks.models import TaskStatus

logger = TransactionManagerAppLoggerFactory.get()


@celery.task(queue='file_system_tasks', bind=True)
def excel_to_mongodb_data_ingestion_task(self: Task, filepath: str, excel_sheet_name: Optional[str]) \
        -> Union[str, TaskStatus]:
    """
    Task that wraps the data ingestion from excel file to mongodb. Responsible for task status management.

    :param filepath: The excel filepath to load.
    :param excel_sheet_name: The excel sheet name.

    :return Either a string message when the service run successfully or a
    """
    logger.info("Loading data from {0} to MongoDB, task id {1}.".format(filepath, self.request.id))

    self.update_state(state=states.STARTED)

    return get_excel_to_mongodb_data_ingestion_service().apply(
        filepath=filepath,
        excel_sheet_name=excel_sheet_name
    )
