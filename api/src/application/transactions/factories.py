from application.transactions.repository import TransactionRepository
from application.transactions.services import GetTransactionsGroupedByService


def get_transactions_group_by_service() -> GetTransactionsGroupedByService:
    return GetTransactionsGroupedByService(
        transaction_repository=TransactionRepository()
    )
