from pathlib import Path

import pytest

from terraland.infrastructure.file_system.services import FileSystemService


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Fixture to provide a temporary directory for testing"""
    return tmp_path


@pytest.fixture
def file_system_service(temp_dir):
    """Fixture to provide a FileSystemService instance"""
    return FileSystemService(temp_dir)


@pytest.fixture
def temp_dir_with_files(tmp_path: Path) -> Path:
    """Fixture to provide a temporary directory with files for testing"""
    try:
        (tmp_path / "test1.tfstate").touch()
        (tmp_path / "subfolder").mkdir(exist_ok=True)
        (tmp_path / "subfolder" / "test2.tfstate").touch()
        (tmp_path / "not_state.txt").touch()
        (tmp_path / "main.tf").touch()
    except OSError as e:
        pytest.fail(f"Failed to set up test files: {e}")
    return tmp_path


@pytest.fixture
def file_system_service_with_grep_files(file_system_service):
    """Fixture to provide a FileSystemService instance with files for testing"""
    (file_system_service.work_dir / "main.tf").touch()
    (file_system_service.work_dir / "file.tf").touch()

    grep_results = [
        f"{file_system_service.work_dir}/file.tf:1:resource aws_instance",
        f"{file_system_service.work_dir}/main.tf:5:resource aws_s3",
    ]

    file_system_service._mocked_grep_results = grep_results

    return file_system_service
