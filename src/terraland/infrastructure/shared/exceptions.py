class CommandExecutionException(Exception):
    """
    Represents an exception raised during command execution.

    This exception is specifically used to signal errors that occur
    while attempting to execute a command. It allows the encapsulation
    of error details associated with the failure of a command's execution.

    Attributes:
        message (str): The error message describing what went wrong.
    """
