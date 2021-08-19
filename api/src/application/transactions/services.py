from typing import List, Union, Dict

from pyspark import Row

from application.transactions.repository import TransactionRepository
import itertools


class GetTransactionsGroupedByService:

    def __init__(
            self,
            transaction_repository: TransactionRepository
    ):
        self.transaction_repository: TransactionRepository = transaction_repository

    def apply(self) -> List[Dict[str, Union[str, List[str]]]]:
        """
        Groups Transactions by Invoice No and returns a list of the grouped information.

        :return A list containing the grouped transactions. Format:
            1. 'invoice_no': The Invoice No.
            2. '_ids': A list containing the rows corresponding to the Invoice No group.
        """
        grouped_by_invoice_transactions: List[Row] = self.transaction_repository.get_grouped_invoice_transactions()

        return [
            {
                'invoice_no': x[0],
                '_ids': list(itertools.chain.from_iterable(x[1]))
            } for x in grouped_by_invoice_transactions
        ]
