from fastapi import APIRouter

from application.tasks.models import TaskStatus
from application.tasks.services import GetTaskStatusReportService

router = APIRouter()


@router.get("/task-status/{task_id}")
async def get_task_status_details(task_id) -> TaskStatus:
    """
    Entrypoint for celery task status monitoring.

    :param task_id: The celery task id.
    :return The task status report.
    """
    return GetTaskStatusReportService().apply(task_id=task_id)
