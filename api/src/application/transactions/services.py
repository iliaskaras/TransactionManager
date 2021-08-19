from typing import List, Union, Dict

from pyspark import Row

from application.infrastructure.error.errors import InvalidArgumentError, NoneArgumentError
from application.transactions.enums import TransactionColumns
from application.transactions.errors import TransactionNotFoundError
from application.transactions.repository import TransactionRepository
import itertools


class GetTransactionsGroupedByService:

    def __init__(
            self,
            transaction_repository: TransactionRepository
    ):
        self.transaction_repository: TransactionRepository = transaction_repository

    def apply(self, group_by_cols: List[str], sort: bool = True) -> List[Dict[str, Union[str, List[str]]]]:
        """
        Groups Transactions by Invoice No and returns a list of the grouped information.

        :param group_by_cols: The columns to group by.
        :param sort: Sort flag indicating if we want our aggregated group by results to be sorted.

        :return A list containing the grouped transactions. Format:
            1. 'invoice_no': The Invoice No.
            2. '_ids': A list containing the rows corresponding to the Invoice No group.
        """
        if not group_by_cols:
            raise NoneArgumentError("At least one group-by column is required.")
        if type(sort) is not bool:
            raise InvalidArgumentError("Invalid sort is provided.")

        for col in group_by_cols:
            if col not in TransactionColumns.values():
                raise InvalidArgumentError(
                    '"{}" is not a transaction field. Choose among: {}'.format(
                        col,
                        TransactionColumns.values()
                    )
                )

        grouped_by_invoice_transactions: List[Row] = self.transaction_repository.group_by(
            group_by_cols=group_by_cols,
            aggregated_col='_id',
            sort=sort
        )

        return [
            {
                'invoice_no': x[0],
                '_ids': list(itertools.chain.from_iterable(x[1]))
            } for x in grouped_by_invoice_transactions
        ]


class GetMostSoldStockCodeService:

    def __init__(
            self,
            transaction_repository: TransactionRepository
    ):
        self.transaction_repository: TransactionRepository = transaction_repository

    def apply(self) -> Dict[str, Union[str, int]]:
        """
        Return the most sold stock code from the transactions.

        :return The the most sold stock code (product) with its total sold quantity. Example:
            {'stock_code': <stock-code>, 'total_sold': <sum-of-all-the-quantities>}

        :raises TransactionNotFoundError: In case repository returned zero rows.
        """
        most_sold_stock_code: Row = self.transaction_repository.get_most_sold_stock_code()

        if not most_sold_stock_code:
            raise TransactionNotFoundError(
                "It wasn't possible to find any transaction when trying to find "
                "out the most sold stock code."
            )

        return {
            'stock_code': most_sold_stock_code[0],
            'total_sold': most_sold_stock_code[1]
        }


class GetCustomerWithMostSpentMoneyService:

    def __init__(
            self,
            transaction_repository: TransactionRepository
    ):
        self.transaction_repository: TransactionRepository = transaction_repository

    def apply(self) -> Dict[str, Union[str, int]]:
        """
        Return the customer with the most spent money.

        :return The customer with the most total spent money. Example:
            {'customer_id': <customer-id>, 'total_spent': <sum-of-all-the-transaction-unit-prices>}

        :raises TransactionNotFoundError: In case repository returned zero rows.
        """
        customer: Row = self.transaction_repository.get_customer_with_most_spent_money()

        if not customer:
            raise TransactionNotFoundError(
                "It wasn't possible to find any transaction when trying to find "
                "out the customer witht he most spent money."
            )

        return {
            'customer_id': customer[0],
            'total_spent': customer[1]
        }


class GetAverageUnitPriceService:

    def __init__(
            self,
            transaction_repository: TransactionRepository
    ):
        self.transaction_repository: TransactionRepository = transaction_repository

    def apply(self) -> Dict[str, Union[str, int]]:
        """
        Return the average unit price.

        :return The average unit price. Example:
            {'averege_unit_price': <average>}

        """
        row: Row = self.transaction_repository.get_average_unit_price()

        return {
            'averege_unit_price': row[0],
        }


class GetPriceAndQuantityRatioService:

    def __init__(
            self,
            transaction_repository: TransactionRepository
    ):
        self.transaction_repository: TransactionRepository = transaction_repository

    def apply(self) -> List[Dict[str, Union[str, float]]]:
        """
        Return the ratio between price and quantity for each invoice.

        :return The ratio between price and quantity for each invoice. Example:
        [
            {
                'invoice_no': <invoice-id1>,
                'ratio': <ratio>
            },
            {
                'invoice_no': <invoice-id2>,
                'ratio': <ratio>
            }
        ]
        """
        rows: List[Row] = self.transaction_repository.get_price_and_quantity_ratio()

        return [
            {
                'invoice_no': x[0],
                'ratio': x[1]
            } for x in rows
        ]
