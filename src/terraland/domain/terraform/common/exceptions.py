class BaseTerraformException(Exception):
    """
    Base exception for Terraform Core related errors.

    This class serves as the base exception for handling errors specifically related
    to Terraform Core functionality. It is intended to be extended by more specific
    exception classes that provide clearer context for particular error cases.

    Arguments:
        command: The Terraform command that resulted in the error.
        message: A descriptive message providing details about the error.n.
    """

    def __init__(self, command: str, message: str):
        self.command = command
        self.message = message
        super().__init__(message)
