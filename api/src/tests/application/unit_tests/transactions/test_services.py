import pytest
from typing import Optional, List
from unittest.mock import MagicMock

from pyspark import Row

from application.infrastructure.error.errors import InvalidArgumentError, NoneArgumentError, TransactionManagerBaseError
from application.transactions.enums import TransactionColumns
from application.transactions.errors import TransactionNotFoundError
from application.transactions.services import GetTransactionsGroupedByService, GetMostSoldStockCodeService, \
    GetCustomerWithMostSpentMoneyService, GetAverageUnitPriceService, GetPriceAndQuantityRatioService


class TestGetTransactionsGroupedByService:

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.mock_transaction_repository = MagicMock()

        self.get_transactions_grouped_by_service = GetTransactionsGroupedByService(self.mock_transaction_repository)

    @pytest.mark.parametrize('group_by_cols, sort, error', [
        # when_group_by_cols_is_none
        (None, False, NoneArgumentError('At least one group-by column is required.')),
        # when_sort_is_none
        (['InvoiceNo'], None, InvalidArgumentError('The Filter ID is required.')),
        # when_sort_is_not_of_bool_type
        (['InvoiceNo'], 'str', InvalidArgumentError('Invalid sort is provided.')),
        # when_group_by_cols_are_not_correct
        (
                ['NonExistingColumn'],
                True,
                InvalidArgumentError(
                    '"NonExistingColumn" is not a transaction field. Choose among: {}'.format(
                        TransactionColumns.values())
                )
        ),
    ])
    def test_apply_with_invalid_arguments(
            self,
            group_by_cols: Optional[List[str]],
            sort: Optional[bool],
            error: TransactionManagerBaseError
    ) -> None:
        with pytest.raises(TransactionManagerBaseError) as ex:
            self.get_transactions_grouped_by_service.apply(
                group_by_cols=group_by_cols,
                sort=sort
            )
        assert ex.value.__dict__ == error.__dict__

    def test_apply(self) -> None:
        rows: List = [
            ('invoice1', [Row('611da7d2f71fed4cd5413f5b'), Row('611da7d2f71fed4cd5413f5a')]),
            ('invoice2', [Row('611da7d2f71fed4cd5413f5b'), Row('611da7d2f71fed4cd5413f5a')]),
        ]

        expected_result = [
            {
                'invoice_no': 'invoice1',
                '_ids': ['611da7d2f71fed4cd5413f5b', '611da7d2f71fed4cd5413f5a']
            },
            {
                'invoice_no': 'invoice2',
                '_ids': ['611da7d2f71fed4cd5413f5b', '611da7d2f71fed4cd5413f5a']
            }
        ]
        self.mock_transaction_repository.group_by.return_value = rows

        assert self.get_transactions_grouped_by_service.apply(
            group_by_cols=TransactionColumns.values(),
            sort=True
        ) == expected_result

        self.mock_transaction_repository.group_by.assert_called_once_with(
            group_by_cols=TransactionColumns.values(),
            aggregated_col='_id',
            sort=True
        )


class TestGetMostSoldStockCodeService:

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.mock_transaction_repository = MagicMock()

        self.get_most_sold_stock_code_service = GetMostSoldStockCodeService(self.mock_transaction_repository)

    def test_apply_raise_error_when_transaction_do_not_exist(self) -> None:
        self.mock_transaction_repository.get_most_sold_stock_code.return_value = None

        with pytest.raises(TransactionNotFoundError) as ex:
            self.get_most_sold_stock_code_service.apply()

        assert ex.value.__dict__ == TransactionNotFoundError(
            "It wasn't possible to find any transaction when trying to find "
            "out the most sold stock code."
        ).__dict__

        self.mock_transaction_repository.get_most_sold_stock_code.assert_called_once()

    def test_apply(self) -> None:
        row: Row = Row(StockCode='1', total_quantities=10)

        expected_result = {
            'stock_code': '1',
            'total_sold': 10
        }

        self.mock_transaction_repository.get_most_sold_stock_code.return_value = row

        assert self.get_most_sold_stock_code_service.apply() == expected_result

        self.mock_transaction_repository.get_most_sold_stock_code.assert_called_once()


class TestGetCustomerWithMostSpentMoneyService:

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.mock_transaction_repository = MagicMock()

        self.get_customer_with_most_spent_money_service = GetCustomerWithMostSpentMoneyService(
            self.mock_transaction_repository
        )

    def test_apply_raise_error_when_transaction_do_not_exist(self) -> None:
        self.mock_transaction_repository.get_customer_with_most_spent_money.return_value = None

        with pytest.raises(TransactionNotFoundError) as ex:
            self.get_customer_with_most_spent_money_service.apply()

        assert ex.value.__dict__ == TransactionNotFoundError(
            "It wasn't possible to find any transaction when trying to find "
            "out the customer witht he most spent money."
        ).__dict__

        self.mock_transaction_repository.get_customer_with_most_spent_money.assert_called_once()

    def test_apply(self) -> None:
        row: Row = Row(CustomerID='10', total_spent=100.0)

        expected_result = {
            'customer_id': '10',
            'total_spent': 100.0
        }

        self.mock_transaction_repository.get_customer_with_most_spent_money.return_value = row

        assert self.get_customer_with_most_spent_money_service.apply() == expected_result

        self.mock_transaction_repository.get_customer_with_most_spent_money.assert_called_once()


class TestGetAverageUnitPriceService:

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.mock_transaction_repository = MagicMock()

        self.get_average_unit_price_service = GetAverageUnitPriceService(
            self.mock_transaction_repository
        )

    def test_apply(self) -> None:
        row: Row = Row(5.0)

        expected_result = {
            'averege_unit_price': 5.0
        }

        self.mock_transaction_repository.get_average_unit_price.return_value = row

        assert self.get_average_unit_price_service.apply() == expected_result

        self.mock_transaction_repository.get_average_unit_price.assert_called_once()


class TestGetPriceAndQuantityRatioService:

    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.mock_transaction_repository = MagicMock()

        self.get_price_and_quantity_ratio_service = GetPriceAndQuantityRatioService(
            self.mock_transaction_repository
        )

    def test_apply(self) -> None:
        rows: List[Row] = [
            Row(invoice_no='invoice1', ratio=0.1),
            Row(invoice_no='invoice2', ratio=0.2),
        ]

        expected_result = [
            {
                'invoice_no': 'invoice1',
                'ratio': 0.1
            },
            {
                'invoice_no': 'invoice2',
                'ratio': 0.2
            },
        ]

        self.mock_transaction_repository.get_price_and_quantity_ratio.return_value = rows

        assert self.get_price_and_quantity_ratio_service.apply() == expected_result

        self.mock_transaction_repository.get_price_and_quantity_ratio.assert_called_once()
