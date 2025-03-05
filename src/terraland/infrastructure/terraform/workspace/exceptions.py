from terraland.domain.terraform.workspaces.exceptions import (
    BaseTerraformWorkspaceException,
)


class TerraformWorkspaceListException(BaseTerraformWorkspaceException):
    """
    Represents an exception related to Terraform workspace operations.

    This class acts as a customized exception used throughout the application
    to handle various errors related to Terraform workspace management.
    It inherits from BaseTerraformWorkspaceException to ensure consistent
    error handling and provide a foundation for future workspace-specific
    exceptions.
    """


class TerraformWorkspaceSwitchException(BaseTerraformWorkspaceException):
    """
    Represents an exception related to Terraform workspace operations.

    This class acts as a customized exception used throughout the application
    to handle various errors related to Terraform workspace management.
    It inherits from BaseTerraformWorkspaceException to ensure consistent
    error handling and provide a foundation for future workspace-specific
    exceptions.
    """
