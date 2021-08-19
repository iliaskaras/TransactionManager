from typing import List

from pyspark import Row
from pyspark.sql import DataFrame

from application.infrastructure.database.repository import BaseSparkRepository


class TransactionRepository(BaseSparkRepository):

    def get_grouped_invoice_transactions(self) -> List[Row]:
        """
        Returns the Transactions grouped by InvoiceNo.

        :return A list of Rows containing:
            1) 'invoice_no': The invoice number.
            2) '_ids': The Transaction MongoDB ids corresponding to the grouped transactions.
        """
        group_pipeline = "{'$group': {'_id': '$InvoiceNo', 'invoices': {'$push': '$_id'}}}"

        df: DataFrame = self.spark_session.read.format("mongo").option("pipeline", group_pipeline).load()
        return df.collect()

