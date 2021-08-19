from typing import List, Optional

from pyspark import Row
import pyspark.sql.functions as f

from application.infrastructure.database.repository import BaseSparkRepository
from pyspark.sql.functions import sort_array, collect_list
from pyspark.sql.functions import sum as pyspark_sum


class TransactionRepository(BaseSparkRepository):

    def group_by(
            self,
            group_by_cols: List[str],
            aggregated_col: Optional[str] = '_id',
            sort: bool = True
    ) -> List[Row]:
        """
        Returns the Transactions grouped by the provided columns.

        :param group_by_cols: The columns to group by.
        :param aggregated_col: The column to aggregate the results.
        :param sort: Sort flag indicating if we want our aggregated group by results to be sorted.

        :return A list of Rows containing:
            1) 'invoice_no': The invoice number.
            2) '_ids': The Transaction MongoDB ids corresponding to the grouped transactions.
        """
        if sort:
            return self.spark_session.read.format("mongo").load().groupBy(
                group_by_cols
            ).agg(sort_array(collect_list(aggregated_col))).collect()
        else:
            return self.spark_session.read.format("mongo").load().groupBy(
                group_by_cols
            ).agg(collect_list(aggregated_col)).collect()

    def get_most_sold_stock_code(self) -> Row:
        """
        Returns the most sold stock code.

        :return A Row containing:
            1) 'stock_code': The most sold stock code.
            2) 'total_sold': The sum of the stock code quantities.
        """
        return self.spark_session.read.format("mongo").load().groupBy(
            'StockCode'
        ).agg(pyspark_sum('Quantity').name('total_quantities')).sort('total_quantities', ascending=False).first()

    def get_customer_with_most_spent_money(self) -> Row:
        """
        Return the customer with the most spent money.
        Operations happening in the call:
        1. Group transactions by CustomerID, StockCode, UnitPrice, Quantity.
        2. Calculate for each Customer's StockCode, the total spent, aggregation result example:
            Row(CustomerID='13693', StockCode='22776', UnitPrice=9.95, Quantity=-1, total_spent_for_stock_code=-9.95)
            Row(CustomerID='13693', StockCode='22766', UnitPrice=2.95, Quantity=-1, total_spent_for_stock_code=-2.95)
            Row(CustomerID='13693', StockCode='84819', UnitPrice=4.25, Quantity=-1, total_spent_for_stock_code=-4.25)
            Row(CustomerID='13693', StockCode='22325', UnitPrice=4.95, Quantity=-3, total_spent_for_stock_code=-14.850000000000001)
        3. Finally sum all the totals from step (2), meaning, the total spent for all the Customer bought StockCodes,
        and sort to get the customer with the most spent. Result example:
            Row(CustomerID='13693', total_spent=-32.0)

            We have total_spent=-32.0 which can be verified by the sum of step (2) results:
            -9,95-2,95-4,25-14,850000000000001 = -32

        :return A Row containing:
            1) 'customer_id': The customer id.
            2) 'total_spent': The sum of the total money spent.
        """

        return self.spark_session.read.format("mongo").load() \
            .filter("CustomerID is not NULL") \
            .groupby(['CustomerID', 'StockCode', 'UnitPrice', 'Quantity']) \
            .agg(f.expr('UnitPrice*Quantity').alias('total_spent_for_stock_code')) \
            .groupby(['CustomerID']) \
            .agg(pyspark_sum('total_spent_for_stock_code').name('total_spent')) \
            .sort('total_spent', ascending=False) \
            .first()

    def get_average_unit_price(self) -> Row:
        """
        Returns the average unit price.

        :return A Row containing the average unit price.
        """

        return self.spark_session.read.format("mongo").load() \
            .groupby() \
            .avg('UnitPrice').first()

    def get_price_and_quantity_ratio(self) -> List[Row]:
        """
        Returns the ratio between price and quantity for each invoice.

        :return A Rows containing the ratio between price and quantity for each invoice:
            1) 'InvoiceNo': The invoice id.
            2) 'ratio': The ratio.
        """
        return self.spark_session.read.format("mongo").load() \
            .groupby(['InvoiceNo', 'UnitPrice', 'Quantity']) \
            .agg(f.expr('UnitPrice/Quantity').alias('ratio')) \
            .select(['InvoiceNo', 'ratio']).withColumnRenamed('InvoiceNo', 'invoice_no') \
            .collect()
