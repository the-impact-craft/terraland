from dataclasses import dataclass

from terraland.domain.terraform.common.entities import BaseTerraformOutput


@dataclass(frozen=True)
class Workspace:
    """
    Represents a workspace entity for organizational and management purposes.

    This class provides a structure to define and manage workspaces, including
    functionalities related to activation status.

    Attributes:
        name (str): The name of the workspace.
        is_active (bool): A flag indicating whether the workspace is currently active.
    """

    uuid: str
    name: str
    is_active: bool = False


@dataclass
class WorkspaceListOutput(BaseTerraformOutput):
    """
    Represents the output of a Terraform workspace list operation.

    This class is designed to store and organize the list of available
    workspaces and the workspace currently selected. It is a data container
    primarily used in Terraform-related operations to represent the state
    of workspaces within a Terraform project.

    Attributes:
        workspaces (list[Workspace]): A list of workspace entities, including the active workspace.
    """

    workspaces: list[Workspace]
