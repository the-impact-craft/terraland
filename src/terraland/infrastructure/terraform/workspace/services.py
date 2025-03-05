import subprocess
import uuid
from pathlib import Path

from terraland.domain.terraform.workspaces.entities import Workspace, WorkspaceListOutput
from terraland.domain.terraform.workspaces.services import BaseWorkspaceService
from terraland.infrastructure.shared.command_utils import clean_up_command_output
from terraland.infrastructure.terraform.workspace.exceptions import (
    TerraformWorkspaceListException,
    TerraformWorkspaceSwitchException,
)


class WorkspaceService(BaseWorkspaceService):
    TERRAFORM_NOT_FOUND_MESSAGE = "Terraform command not found. Is it installed and in PATH?"

    def __init__(self, work_dir: str | Path, *args, **kwargs):
        self.work_dir = work_dir if isinstance(work_dir, str) else str(work_dir)
        super().__init__(*args, **kwargs)

    def list(self) -> WorkspaceListOutput:
        """
        List all Terraform workspaces.

        Executes the 'terraform workspace list' command and returns a list of workspace names.

        Returns:
            WorkspaceListOutput: A data class containing the list of workspaces and the command executed.

        Raises:
            TerraformWorkspaceException: If an error occurs while listing workspaces.

        Example:
            workspaces = workspace.list()  # Returns a list of available workspaces

        """

        command = ["terraform", "workspace", "list"]
        command_str = " ".join(command)
        try:
            result = subprocess.run(
                command,
                cwd=self.work_dir,
                capture_output=True,
                text=True,
                check=True,
            )
            # Handle the * prefix that indicates current workspace
            workspaces = [
                Workspace(
                    uuid=f"id-{uuid.uuid5(uuid.NAMESPACE_DNS, workspace.strip().lstrip('* '))}",
                    name=workspace.strip().lstrip("* "),
                    is_active="*" in workspace,
                )
                for workspace in result.stdout.split("\n")
                if workspace.strip()
            ]
            return WorkspaceListOutput(workspaces=workspaces, command=command_str)
        except subprocess.CalledProcessError as e:
            raise TerraformWorkspaceListException(command_str, clean_up_command_output(e.stderr))
        except FileNotFoundError:
            raise TerraformWorkspaceListException(command_str, self.TERRAFORM_NOT_FOUND_MESSAGE)
        except Exception as e:
            raise TerraformWorkspaceListException(command_str, clean_up_command_output(str(e)))

    # TODO: remove pragma once the method is implemented
    def create(self, name: str):  # pragma: no cover
        """
        Create a new Terraform workspace with the specified name.

        This method validates the workspace name and uses the Terraform CLI to create a new workspace.
        It ensures the workspace name is non-empty and handles potential command execution errors.

        Parameters:
            name (str): The name of the new Terraform workspace to create.
                        Must be a non-empty string after stripping whitespace.

        Returns:
            str: The output from the Terraform workspace creation command, with whitespace stripped.

        Raises:
            ValueError: If the provided workspace name is empty or contains only whitespace.
            RuntimeError: If the Terraform workspace creation command fails, with details of the error.

        Example:
            workspace = WorkspaceService()
            result = workspace.create('my-new-workspace')  # Creates a new workspace named 'my-new-workspace'
        """
        if not name or not name.strip():
            raise ValueError("Workspace name cannot be empty")

        try:
            result = subprocess.run(
                ["terraform", "workspace", "new", name],
                capture_output=True,
                text=True,
                check=True,
                cwd=self.work_dir,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to create workspace '{name}': {e.stderr}")

    def switch(self, name: str):
        """
        Switch to a specific Terraform workspace.

        Selects the specified workspace using the Terraform CLI. Validates the workspace name
        to ensure it is not empty or whitespace-only.

        Parameters:
            name (str): The name of the Terraform workspace to switch to.

        Raises:
            TerraformWorkspaceSwitchException: If an error occurs while switching workspaces.

        Example:
            workspace = WorkspaceService()
            workspace.switch('development')  # Switches to the 'development' workspace
        """
        if not name or not name.strip():
            raise ValueError("Workspace name cannot be empty")

        command = ["terraform", "workspace", "select", name]
        command_str = " ".join(command)
        try:
            subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                cwd=self.work_dir,
            )
        except subprocess.CalledProcessError as e:
            raise TerraformWorkspaceSwitchException(command_str, clean_up_command_output(e.stderr))
        except Exception as e:
            raise TerraformWorkspaceSwitchException(command_str, clean_up_command_output(str(e)))
