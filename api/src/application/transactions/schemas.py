from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType, DoubleType

schema = StructType([
    StructField('InvoiceNo', StringType(), False),
    StructField('StockCode', StringType(), False),
    StructField('Description', StringType(), True),
    StructField('Quantity', IntegerType(), False),
    StructField('InvoiceDate', DateType(), False),
    StructField('UnitPrice', DoubleType(), False),
    StructField('CustomerID', StringType(), True),
    StructField('Country', StringType(), False),
])