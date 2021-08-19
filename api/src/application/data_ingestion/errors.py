from application.infrastructure.error.errors import TransactionManagerBaseError


class ExcelFileLoadingError(TransactionManagerBaseError):
    pass


class MongoDBDataWriteError(TransactionManagerBaseError):
    pass
