from terraland.domain.terraform.core.exceptions import BaseTerraformCoreException


class TerraformVersionException(BaseTerraformCoreException):
    """
    Exception raised for invalid Terraform version.

    This exception is specifically used when an invalid or unsupported Terraform
    version is encountered. It allows the user to handle version-related errors
    associated with Terraform operations and ensures that appropriate actions
    can be taken. This class inherits from BaseTerraformCoreException.
    """


class TerraformFormatException(BaseTerraformCoreException):
    """
    Exception raised for invalid Terraform formatting operation.

    This exception is used when an error occurs during Terraform formatting
    operations. It provides a way to handle formatting-related errors and
    ensures that the user can take appropriate actions to rectify the issue.
    This class inherits from BaseTerraformCoreException.
    """


class TerraformPlanException(BaseTerraformCoreException):
    """
    Exception raised for invalid Terraform plan operation.

    This exception is used when an error occurs during Terraform plan operations.
    It provides a way to handle plan-related errors and ensures that the user can
    take appropriate actions to rectify the issue. This class inherits from
    BaseTerraformCoreException.
    """


class TerraformInitException(BaseTerraformCoreException):
    """
    Exception raised for invalid Terraform init operation.

    This exception is used when an error occurs during Terraform init operations.
    It provides a way to handle init-related errors and ensures that the user can
    take appropriate actions to rectify the issue. This class inherits from
    BaseTerraformCoreException.
    """


class TerraformValidateException(BaseTerraformCoreException):
    """
    Represents an exception specific to Terraform validation errors.

    This exception is a specialized child of BaseTerraformCoreException, specifically
    designed for cases where Terraform validation processes encounter issues. It can
    be utilized in scenarios requiring explicit handling of validation-related errors
    within the Terraform workflow or process.
    """
