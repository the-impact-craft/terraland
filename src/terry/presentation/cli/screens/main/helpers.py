import os
from datetime import datetime

from terry.infrastructure.terraform.core.exceptions import TerraformVersionException
from terry.settings import STATUS_TO_ICON, CommandStatus


def validate_work_dir(path) -> None:
    """
    Validate the provided working directory path.

    This method checks if the provided path exists, is a directory, and is readable.

    Parameters:
        path (Path): The working directory path to validate.

    Raises:
        ValueError: If the path does not exist or is not a directory.
        PermissionError: If the directory is not readable.

    """
    if not path.exists():
        raise ValueError(f"Directory does not exist: {path}")

    if not path.is_dir():
        raise ValueError(f"Path is not a directory: {path}")

    if not os.access(path, os.R_OK):
        raise PermissionError(f"Directory is not readable: {path}")


def get_or_raise_validate_terraform(terraform_core_service):
    """
    Validate the Terraform installation in the current environment.

    This method checks if the Terraform binary is available in the system PATH.

    Raises:
        RuntimeError: If the Terraform binary is not found in the system PATH.
        RuntimeError: If the version output cannot be parsed.
    """

    try:
        return terraform_core_service.version()
    except TerraformVersionException as e:
        error_message = f"""Terraform seems to be not installed. 
            Please install Terraform to use this application. 
            Details: {str(e)}"""
        raise RuntimeError(error_message)


class CommandLogMessageFormatter:
    @staticmethod
    def get_primary_message(message: str) -> str:
        return f"~$: [bold]{message}[/bold]"

    @staticmethod
    def get_secondary_message(message: str) -> str:
        return f"[#808080]{message}[/#808080]"

    @staticmethod
    def get_datetime_status_message(
        message: str,
        status: CommandStatus,
    ) -> str:
        return f"{STATUS_TO_ICON.get(status)} [#808080]{datetime.now()} {message} [/#808080][{status.name}]"
