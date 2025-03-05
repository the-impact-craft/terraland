from terraland.domain.terraform.common.exceptions import BaseTerraformException


class BaseTerraformWorkspaceException(BaseTerraformException):
    """
    Base exception class for Terraform workspace-related errors.

    This class provides a foundation for defining exceptions that are specific
    to issues and errors encountered within the Terraform workspace context. It
    extends the base Terraform exception class, allowing for workspace-specific
    exception handling in Terraform operations.

    Arguments:
        command: The Terraform command that resulted in the error.
        message: A descriptive message providing details about the error.
    """
