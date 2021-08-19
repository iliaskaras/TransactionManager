from typing import Optional

from pydantic import BaseModel


class Transaction(BaseModel):
    invoice_no: Optional[str]
    stock_code: Optional[str]
    description: Optional[str]
    quantity: Optional[int]
    invoice_date: Optional[str]
    unit_price: Optional[float]
    customer_id: Optional[str]
    country: Optional[str]
