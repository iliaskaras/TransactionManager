from celery.result import AsyncResult

from application.infrastructure.error.errors import NoneArgumentError
from application.infrastructure.loggers.loggers import TransactionManagerAppLoggerFactory
from application.tasks.models import TaskStatus

logger = TransactionManagerAppLoggerFactory.get()


class GetTaskStatusReportService:

    def apply(self, task_id: str) -> TaskStatus:
        """
        Reports the task id state details.

        :param task_id: The Celery task id.
        :return TaskStatus: The Task status details.

        :raises NoneArgumentError: When task_id is not provided.
        """
        if not task_id:
            raise NoneArgumentError("Task id is required.")

        task_result = AsyncResult(task_id)

        return TaskStatus(
            task_id=task_id,
            task_status=task_result.status,
            task_result=task_result.result
        )
