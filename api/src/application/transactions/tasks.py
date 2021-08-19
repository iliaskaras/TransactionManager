from typing import Union, Dict, List

from celery import states, Task

from application.celery_worker import celery
from application.infrastructure.loggers.loggers import TransactionManagerAppLoggerFactory
from application.transactions.factories import get_transactions_group_by_service

logger = TransactionManagerAppLoggerFactory.get()


@celery.task(queue='transaction_tasks', bind=True)
def get_grouped_invoice_transactions_task(self: Task) -> List[Dict[str, Union[str, List[str]]]]:
    """
    Task that wraps the transaction group by invoice no. Responsible for task status management.

    :return A list containing the grouped transactions. Format:
        1. 'invoice_no': The Invoice No.
        2. '_ids': A list containing the rows corresponding to the Invoice No group.
    """
    logger.info("Retrieving group by Invoice No transactions, task id {0}.".format(self.request.id))
    self.update_state(state=states.STARTED)
    return get_transactions_group_by_service().apply()
