class TransactionManagerBaseError(Exception):
    pass


class ArgumentError(TransactionManagerBaseError):
    message = "Argument error."
    error_type = "ArgumentError"


class InvalidArgumentError(ArgumentError):
    message = "Invalid argument error."
    error_type = "InvalidArgumentError"


class NoneArgumentError(ArgumentError):
    message = "Missing argument error."
    error_type = "MissingArgumentError"


class ValidationError(TransactionManagerBaseError):
    message = "Validation error."
    error_type = "ValidationError"
