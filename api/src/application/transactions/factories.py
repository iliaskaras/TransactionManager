from application.transactions.repositories import TransactionRepository
from application.transactions.services import GetTransactionsGroupedByService, GetMostSoldStockCodeService, \
    GetCustomerWithMostSpentMoneyService, GetAverageUnitPriceService, GetPriceAndQuantityRatioService


def get_transactions_group_by_service() -> GetTransactionsGroupedByService:
    return GetTransactionsGroupedByService(
        transaction_repository=TransactionRepository()
    )


def get_most_sold_stock_code_service() -> GetMostSoldStockCodeService:
    return GetMostSoldStockCodeService(
        transaction_repository=TransactionRepository()
    )


def get_customer_with_most_spent_money_service() -> GetCustomerWithMostSpentMoneyService:
    return GetCustomerWithMostSpentMoneyService(
        transaction_repository=TransactionRepository()
    )


def get_average_unit_price_service() -> GetAverageUnitPriceService:
    return GetAverageUnitPriceService(
        transaction_repository=TransactionRepository()
    )


def get_price_and_quantity_ratio_service() -> GetPriceAndQuantityRatioService:
    return GetPriceAndQuantityRatioService(
        transaction_repository=TransactionRepository()
    )
