from typing import List

from fastapi import APIRouter, Query

from application.tasks.models import TaskResponseBody
from application.transactions.tasks import get_grouped_invoice_transactions_task, get_most_sold_stock_code_task, \
    get_customer_with_most_spent_money_task, get_average_unit_price_task, get_price_and_quantity_ratio_task

router = APIRouter()


@router.get("/transactions/group", response_description="Group transactions by invoice no endpoint")
async def get_grouped_transactions_by_invoice(
        group_by_cols: List[str] = Query(
            # required.
            ...,
            alias="group-by"
        ),
        sort: bool = True
):
    """
    Entrypoint for returning the transactions grouped by invoice no.

    :return TaskResponseBody.
    """
    task = get_grouped_invoice_transactions_task.delay(
        group_by_cols=group_by_cols,
        sort=sort
    )

    return TaskResponseBody(task_id=task.id)


@router.get("/transactions/most-sold-product", response_description="Get most sold stock code endpoint")
async def get_most_sold_stock_code():
    """
    Entrypoint for returning the most sold stock code.

    :return TaskResponseBody.
    """
    task = get_most_sold_stock_code_task.delay()

    return TaskResponseBody(task_id=task.id)


@router.get("/transactions/best-customer", response_description="Get the customer with the most spent money endpoint")
async def get_customer_with_the_most_spent():
    """
    Entrypoint for returning the customer with the most spent money.

    :return TaskResponseBody.
    """
    task = get_customer_with_most_spent_money_task.delay()

    return TaskResponseBody(task_id=task.id)


@router.get("/transactions/unit-average", response_description="Get the average unit price endpoint")
async def get_average_unit_price():
    """
    Entrypoint for returning the average unit price.

    :return TaskResponseBody.
    """
    task = get_average_unit_price_task.delay()

    return TaskResponseBody(task_id=task.id)


@router.get(
    "/transactions/price-and-quantity-ratio",  response_description="Get the ratio between price and quantity endpoint"
)
async def get_price_and_quantity_ratio():
    """
    Entrypoint for returning the ratio between price and quantity.

    :return TaskResponseBody.
    """
    task = get_price_and_quantity_ratio_task.delay()

    return TaskResponseBody(task_id=task.id)
