from dependency_injector import containers, providers

from terry.infrastructure.file_system.services import FileSystemService
from terry.infrastructure.operation_system.services import OperationSystemService
from terry.infrastructure.terraform.core.services import TerraformCoreService
from terry.infrastructure.terraform.workspace.services import WorkspaceService


class DiContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    file_system_service = providers.Factory(
        FileSystemService,
        work_dir=config.work_dir,
    )

    operation_system_service = providers.Factory(
        OperationSystemService,
    )

    terraform_core_service = providers.Factory(
        TerraformCoreService,
        work_dir=config.work_dir,
        operation_system_service=operation_system_service,
    )

    workspace_service = providers.Factory(
        WorkspaceService,
        work_dir=config.work_dir,
    )
