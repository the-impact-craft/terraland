import pytest

from terraland.domain.terraform.core.entities import PlanSettings
from terraland.infrastructure.terraform.core.services import TerraformCoreService


@pytest.fixture
def terraform_service(temp_dir, operation_system_service):
    """Fixture to provide a TerraformCoreService instance"""
    return TerraformCoreService(temp_dir, operation_system_service)


@pytest.fixture
def plan_empty_settings():
    return PlanSettings()
