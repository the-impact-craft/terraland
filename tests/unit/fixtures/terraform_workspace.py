import pytest

from terraland.infrastructure.terraform.workspace.services import WorkspaceService


@pytest.fixture
def workspace_service(temp_dir):
    """Fixture to provide a WorkspaceService instance"""
    return WorkspaceService(temp_dir)
