from fastapi import APIRouter

from application.tasks.models import TaskResponseBody
from application.transactions.tasks import get_grouped_invoice_transactions_task

router = APIRouter()


@router.get("/transactions/group/", response_description="Group transactions by invoice no endpoint")
async def get_grouped_transactions_by_invoice():
    """
    Entrypoint for returning the transactions grouped by invoice no.

    :return TaskResponseBody.
    """
    task = get_grouped_invoice_transactions_task.delay()

    return TaskResponseBody(task_id=task.id)
