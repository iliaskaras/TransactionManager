from typing import Union, Dict, List, Optional

from celery import states, Task

from application.celery_worker import celery
from application.infrastructure.loggers.loggers import TransactionManagerAppLoggerFactory
from application.transactions.factories import get_transactions_group_by_service, get_most_sold_stock_code_service, \
    get_customer_with_most_spent_money_service, get_average_unit_price_service, get_price_and_quantity_ratio_service

logger = TransactionManagerAppLoggerFactory.get()


@celery.task(queue='transaction_tasks', bind=True)
def get_grouped_invoice_transactions_task(self: Task, group_by_cols: List[str], sort: Optional[bool] = True) \
        -> List[Dict[str, Union[str, List[str]]]]:
    """
    Task that wraps the transaction group by invoice no. Responsible for task status management.

    :param group_by_cols: The columns to group by.
    :param sort: Sort flag indicating if we want our aggregated group by results to be sorted.

    :return A list containing the grouped transactions. Example:
        [
                {
                    "invoice_no": <invoice-no1>,
                    "_ids": [
                        <transaction-id1>,
                        ...
                        <transaction-idK>,
                    ]
                },
                {
                    "invoice_no": <invoice-no2>,
                    "_ids": [
                        <transaction-id1>,
                        ...
                        <transaction-idK>,
                    ]
                },
        ]
    """
    logger.info("Retrieving group by Invoice No transactions, task id {0}.".format(self.request.id))
    self.update_state(state=states.STARTED)
    return get_transactions_group_by_service().apply(group_by_cols=group_by_cols, sort=sort)


@celery.task(queue='transaction_tasks', bind=True)
def get_most_sold_stock_code_task(self: Task) -> Dict[str, Union[str, int]]:
    """
    Task that wraps the retrieval of the most sold stock code. Responsible for task status management.

    :return The the most sold stock code (product) with its total sold quantity. Example:
            {'stock_code': <stock-code>, 'total_sold': <sum-of-all-the-quantities>}
    """
    logger.info("Retrieving the most sold stock product, task id {0}.".format(self.request.id))
    self.update_state(state=states.STARTED)
    return get_most_sold_stock_code_service().apply()


@celery.task(queue='transaction_tasks', bind=True)
def get_customer_with_most_spent_money_task(self: Task) -> Dict[str, Union[str, int]]:
    """
    Task that wraps the retrieval of the customer with the most spent money. Responsible for task status management.

        :return The customer with the most total spent money. Example:
            {'customer_id': <customer-id>, 'total_spent': <sum-of-all-the-transaction-unit-prices>}
    """
    logger.info("Retrieving the most sold stock product, task id {0}.".format(self.request.id))
    self.update_state(state=states.STARTED)
    return get_customer_with_most_spent_money_service().apply()


@celery.task(queue='transaction_tasks', bind=True)
def get_average_unit_price_task(self: Task) -> Dict[str, Union[str, int]]:
    """
    Task that wraps the retrieval of the average unit price. Responsible for task status management.

        :return The average unit price. Example:
            {'averege_unit_price': <average>}
    """
    logger.info("Retrieving the average unit price, task id {0}.".format(self.request.id))
    self.update_state(state=states.STARTED)
    return get_average_unit_price_service().apply()


@celery.task(queue='transaction_tasks', bind=True)
def get_price_and_quantity_ratio_task(self: Task) -> List[Dict[str, Union[str, float]]]:
    """
    Task that wraps the retrieval of the ratio between price and quantity for each invoice.
    Responsible for task status management.

    :return The ratio between price and quantity for each invoice. Example:
        {
            <invoice-no1>: <ratio>,
            ...
            <invoice-noN>: <ratio>
        }
    """
    logger.info("Retrieving the average unit price, task id {0}.".format(self.request.id))
    self.update_state(state=states.STARTED)
    return get_price_and_quantity_ratio_service().apply()
