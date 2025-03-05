from dependency_injector import containers, providers
from diskcache import Cache

from terraland.infrastructure.file_system.services import FileSystemService
from terraland.infrastructure.operation_system.services import OperationSystemService
from terraland.infrastructure.terraform.core.services import TerraformCoreService
from terraland.infrastructure.terraform.workspace.services import WorkspaceService
from terraland.presentation.cli.cache import TerraLandCache


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

    disk_cache = providers.Singleton(Cache, config.cache_dir)

    cache = providers.Factory(
        TerraLandCache,
        cache=disk_cache,
    )
