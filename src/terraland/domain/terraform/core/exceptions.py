from terraland.domain.terraform.common.exceptions import BaseTerraformException


class BaseTerraformCoreException(BaseTerraformException):
    """
    Base exception for Terraform Core related errors.

    This class serves as the base exception for handling errors specifically related
    to Terraform Core functionality. It is intended to be extended by more specific
    exception classes that provide clearer context for particular error cases.

    Arguments:
        command: The Terraform command that resulted in the error.
        message: A descriptive message providing details about the error.n.
    """
