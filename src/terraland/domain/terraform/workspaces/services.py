import abc

from terraland.domain.terraform.workspaces.entities import WorkspaceListOutput


class BaseWorkspaceService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def list(self) -> WorkspaceListOutput:
        """
        List all available Terraform workspaces.

        Returns:
            WorkspaceListOutput: A list of workspace names, with the current workspace potentially marked.

        Raises:
            TerraformWorkspaceException: If an error occurs while listing workspaces."""
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, name: str):
        """
        Create a new Terraform workspace with the specified name.

        Parameters:
            name (str): The name of the new Terraform workspace to create. Must be a non-empty string.

        Raises:
            ValueError: If the workspace name is empty or contains only whitespace.
            RuntimeError: If the Terraform workspace creation command fails, including details of the failure.

        Returns:
            str: The output of the workspace creation command, with leading and trailing whitespace removed.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def switch(self, name: str):
        """
        Switch to a specific Terraform workspace.

        This method selects and activates the specified Terraform workspace by name.

        Parameters:
            name (str): The name of the Terraform workspace to switch to. Must be a non-empty string.

        Raises:
            TerraformWorkspaceSwitchException: If the workspace switch command fails or the workspace does not exist.
        """
        raise NotImplementedError
