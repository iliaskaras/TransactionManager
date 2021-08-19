from enum import Enum
from typing import List


class TransactionColumns(Enum):
    invoice_no = 'InvoiceNo'
    stock_code = 'StockCode'
    description = 'Description'
    quantity = 'Quantity'
    invoice_date = 'InvoiceDate'
    unit_price = 'UnitPrice'
    customer_id = 'CustomerID'
    country = 'Country'

    @classmethod
    def values(cls) -> List[str]:
        return [member.value for member in cls]
