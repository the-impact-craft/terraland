import subprocess
import pytest
from unittest.mock import patch, Mock


from terraland.infrastructure.terraform.workspace.services import WorkspaceService
from terraland.infrastructure.terraform.workspace.exceptions import (
    TerraformWorkspaceListException,
    TerraformWorkspaceSwitchException,
)
from terraland.domain.terraform.workspaces.entities import WorkspaceListOutput


class TestWorkspaceService:
    def test_init_with_string_path(self, temp_dir):
        service = WorkspaceService(str(temp_dir))
        assert isinstance(service.work_dir, str)
        assert service.work_dir == str(temp_dir)

    def test_init_with_path_object(self, temp_dir):
        service = WorkspaceService(temp_dir)
        assert isinstance(service.work_dir, str)
        assert service.work_dir == str(temp_dir)

    def test_list_success(self, workspace_service):
        workspaces = [
            "  default",
            "* development",
            "  production",
        ]
        command = ["terraform", "workspace", "list"]

        mock_result = Mock(stdout="\n".join(workspaces), stderr="", returncode=0)

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            result = workspace_service.list()

            assert isinstance(result, WorkspaceListOutput)
            assert len(result.workspaces) == len(workspaces)
            assert result.command == " ".join(command)

            # Verify workspaces
            workspaces = [(w.name, w.is_active) for w in result.workspaces]
            assert workspaces == [
                ("default", False),
                ("development", True),
                ("production", False),
            ]

            # Verify command execution
            mock_run.assert_called_once_with(
                command, cwd=workspace_service.work_dir, capture_output=True, text=True, check=True
            )

    def test_list_command_error(self, workspace_service):
        error = "Error: Workspace does not exist"
        error_mock = Mock(side_effect=subprocess.CalledProcessError(1, [], stderr=error))
        with patch("subprocess.run", side_effect=error_mock):
            with pytest.raises(TerraformWorkspaceListException) as exc_info:
                workspace_service.list()
            assert error in str(exc_info.value)

    def test_list_terraform_not_found(self, workspace_service):
        with patch("subprocess.run", side_effect=FileNotFoundError()):
            with pytest.raises(TerraformWorkspaceListException) as exc_info:
                workspace_service.list()
            assert workspace_service.TERRAFORM_NOT_FOUND_MESSAGE in str(exc_info.value)

    def test_list_general_error(self, workspace_service):
        with patch("subprocess.run", side_effect=Exception("Unexpected error")):
            with pytest.raises(TerraformWorkspaceListException) as exc_info:
                workspace_service.list()
            assert "Unexpected error" in str(exc_info.value)

    def test_switch_success(self, workspace_service):
        workspace_name = "development"
        mock_result = Mock(stdout=f'Switched to workspace "{workspace_name}".', stderr="", returncode=0)

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            workspace_service.switch(workspace_name)

            mock_run.assert_called_once_with(
                ["terraform", "workspace", "select", workspace_name],
                cwd=workspace_service.work_dir,
                capture_output=True,
                text=True,
                check=True,
            )

    def test_switch_empty_name(self, workspace_service):
        with pytest.raises(ValueError) as exc_info:
            workspace_service.switch("")
        assert "Workspace name cannot be empty" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            workspace_service.switch("   ")
        assert "Workspace name cannot be empty" in str(exc_info.value)

    def test_switch_command_error(self, workspace_service):
        error = 'Error: Workspace "non-existent" doesn\'t exist'
        with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, [], stderr=error)):
            with pytest.raises(TerraformWorkspaceSwitchException) as exc_info:
                workspace_service.switch("non-existent")
            assert error in str(exc_info.value)

    def test_switch_general_error(self, workspace_service):
        with patch("subprocess.run", side_effect=Exception("Unexpected error")):
            with pytest.raises(TerraformWorkspaceSwitchException) as exc_info:
                workspace_service.switch("workspace")
            assert "Unexpected error" in str(exc_info.value)

    # -------------------------------------------------------------------------------------------------------------------
    # Todo: refer to following code snippet after workspace create method is implemented
    # def test_create_success(self, workspace_service):
    #     workspace_name = "new-workspace"
    #     mock_output = f"Created and switched to workspace \"{workspace_name}\"!"
    #     mock_result = Mock(
    #         stdout=mock_output,
    #         stderr="",
    #         returncode=0
    #     )
    #
    #     with patch('subprocess.run', return_value=mock_result) as mock_run:
    #         result = workspace_service.create(workspace_name)
    #
    #         assert result == mock_output
    #         mock_run.assert_called_once_with(
    #             ["terraform", "workspace", "new", workspace_name],
    #             cwd=workspace_service.work_dir,
    #             capture_output=True,
    #             text=True,
    #             check=True
    #         )
    #
    # def test_create_empty_name(self, workspace_service):
    #     with pytest.raises(ValueError) as exc_info:
    #         workspace_service.create("")
    #     assert "Workspace name cannot be empty" in str(exc_info.value)
    #
    #     with pytest.raises(ValueError) as exc_info:
    #         workspace_service.create("   ")
    #     assert "Workspace name cannot be empty" in str(exc_info.value)
    #
    # def test_create_command_error(self, workspace_service):
    #     error = "Error: Workspace already exists"
    #     with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, [], stderr=error)):
    #         with pytest.raises(RuntimeError) as exc_info:
    #             workspace_service.create("existing-workspace")
    #         assert error in str(exc_info.value)
    #
