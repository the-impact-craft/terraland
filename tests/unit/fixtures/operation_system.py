import os

import pytest

from terraland.infrastructure.operation_system.services import OperationSystemService


@pytest.fixture
def operation_system_service():
    """Fixture to provide a OperationSystemService instance"""
    return OperationSystemService()


@pytest.fixture
def mock_environment_variables(monkeypatch):
    """Fixture to mock environment variables."""
    env_vars = {
        "TEST_VAR1": "value1",
        "TEST_VAR2": "value2",
        "FILTER_VAR": "value3",
        "ANOTHER_VAR": "value4",
    }
    monkeypatch.setattr(os, "environ", env_vars)
    return env_vars


@pytest.fixture(autouse=True)
def cleanup_env_vars():
    """Clean up environment variables after each test."""
    initial_env = dict(os.environ)
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(initial_env)
