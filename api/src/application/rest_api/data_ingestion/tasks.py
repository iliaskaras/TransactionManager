from typing import Union, Dict, Optional

from celery import states

from application.celery_worker import celery
from application.infrastructure.loggers.loggers import TransactionManagerAppLoggerFactory
from application.rest_api.data_ingestion.factories import get_excel_to_mongodb_data_ingestion_service

logger = TransactionManagerAppLoggerFactory.get()


@celery.task(queue='file_system_tasks', bind=True)
def data_ingestion_spark_job_task(self, filepath: str, data_address: Optional[str]) -> Union[str, Dict[str, str]]:
    logger.info("Loading into mongo data from {0}, task id {1}.".format(filepath, self.request.id))
    self.update_state(state=states.STARTED)
    try:
        get_excel_to_mongodb_data_ingestion_service().apply(filepath=filepath, data_address=data_address)
    except Exception as ex:
        self.update_state(state=states.FAILURE)
        return {
            'task_status': states.FAILURE,
            'task_id': self.request.id,
            'reason': str(ex)
        }

    return "Data from '{0}' ingested into mongodb successfully.".format(filepath)
