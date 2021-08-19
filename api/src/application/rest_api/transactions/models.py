from typing import Optional, List

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    invoice_no: Optional[str]
    stock_code: Optional[str]
    description: Optional[str]
    quantity: Optional[int]
    invoice_date: Optional[str]
    unit_price: Optional[float]
    customer_id: Optional[str]
    country: Optional[str]


class GroupTransactionsGetRequestParams(BaseModel):
    group_by_cols: List[str] = Field(..., alias='group-by', description='The columns to group by the transactions.')
    sort: Optional[bool] = Field(default=True, description='If we want to sort the aggregated group by results.')

