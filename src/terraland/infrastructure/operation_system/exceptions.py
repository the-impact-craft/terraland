from terraland.domain.operation_system.exceptions import BaseOperationSystemException


class EnvVarOperationSystemException(BaseOperationSystemException):
    """
    Represents an exception class for environment variable operations in the
    operating system.

    This class is a specific exception used to handle errors associated
    with environment variable operations. It extends the base exception
    class `BaseOperationSystemException` and provides an abstraction
    to specifically categorize and identify environment variable-related
    errors in the system.

    """
