import pytest
from textual.css.query import NoMatches
from textual.pilot import Pilot
from textual.widget import Widget
from textual.widgets import RadioSet

from terraland.domain.terraform.workspaces.entities import Workspace
from terraland.infrastructure.terraform.workspace.exceptions import TerraformWorkspaceSwitchException
from terraland.presentation.cli.screens.main.containers.workspaces import Workspaces

# Constants
WORKSPACES_COMPONENT_ID = "#workspaces"
WORKSPACES_RADIO_SET_ID = "#workspaces_radio_set"
ERROR_COMPONENT_NOT_FOUND = "Component {component_id} not found"


class TestWorkspaces:
    """
    Feature: TerraLand Main Screen
        As a user
        I want to interact with the TerraLand interface
        So that I can manage Terraform configurations effectively
    """

    @pytest.mark.asyncio
    async def test_workspaces_list(self, app, workspaces_list):
        """
        Scenario: Render workspaces
            Given multiple Terraform available workspaces
              | workspace   |
              | default     |
              | development |
              | production  |
              And development workspace is active
            When I select the workspaces widget
            Then all available workspaces should be listed in components
            And current workspace is highlighted
        """
        name, index = self.get_active_workspace(workspaces_list)
        statuses = {w.name: w.is_active for w in workspaces_list}

        async with app.run_test() as pilot:
            workspaces_component = self.assert_component_exists(pilot, WORKSPACES_COMPONENT_ID)
            assert workspaces_component.selected_workspace.name == name

            workspaces_radio_set = self.assert_component_exists(pilot, WORKSPACES_RADIO_SET_ID)
            for button in workspaces_radio_set.children:
                assert str(button.label) in statuses  # type: ignore
                assert button.value == statuses[str(button.label)]  # type: ignore

            assert workspaces_radio_set._selected == index  # type: ignore

    @pytest.mark.asyncio
    async def test_switching_between_workspaces(self, app, workspaces_list):
        """
        Scenario: Switching between workspaces
            Given multiple Terraform available workspaces
              | workspace   |
              | default     |
              | development |
              | production  |
            And development workspace is active
            When I select the "default" workspace
            Then the workspace should be switched to "default"
            And the workspace list should show "default" as active
        """
        initial_name, _ = self.get_active_workspace(workspaces_list)
        new_workspace = "default"

        async with app.run_test() as pilot:
            workspaces_component = self.assert_component_exists(pilot, WORKSPACES_COMPONENT_ID)
            await self.select_workspace(pilot, workspaces_component, initial_name, new_workspace)
            assert workspaces_component.selected_workspace.name == new_workspace

    @pytest.mark.asyncio
    async def test_switching_between_workspaces_exception(self, app, workspaces_list):
        """
        Scenario: Error during workspace switching
            Given multiple Terraform available workspaces
            When switching to a new workspace fails
            Then an error message should be displayed
            And the workspace selection should remain unchanged
        """
        new_workspace = "default"
        app.workspace_service.switch.side_effect = TerraformWorkspaceSwitchException(
            message="Failed to switch workspace", command="terraform workspace select"
        )
        initial_name, _ = self.get_active_workspace(workspaces_list)

        async with app.run_test() as pilot:
            workspaces_component = self.assert_component_exists(pilot, WORKSPACES_COMPONENT_ID)
            await self.select_workspace(pilot, workspaces_component, initial_name, new_workspace)
            assert workspaces_component.selected_workspace.name != new_workspace
            assert workspaces_component.selected_workspace.name == initial_name

    # -----------------------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------------------

    @staticmethod
    def get_active_workspace(workspaces: list[Workspace]) -> tuple[str, int]:
        """
        Get the name and index of the active workspace.

        Args:
            workspaces: List of workspace objects

        Returns:
            Tuple of (workspace_name, index) where workspace_name can be None
        """
        selected = next(((i, w) for i, w in enumerate(workspaces) if w.is_active), None)
        return (selected[1].name if selected else "", selected[0] if selected else 0)

    @staticmethod
    def assert_component_exists(pilot: Pilot, component_id: str) -> Widget | Workspaces | RadioSet:
        """
        Helper: Verifies that a component exists, raising a clear error if missing.
        """
        try:
            return pilot.app.query_one(component_id)
        except NoMatches:
            pytest.fail(ERROR_COMPONENT_NOT_FOUND.format(component_id=component_id))

    async def select_workspace(self, pilot: Pilot, workspaces_component: Workspaces, initial: str, new: str):
        """
        Selects and validates a workspace switch.
        """
        assert workspaces_component.selected_workspace.name == initial
        assert initial != new

        workspaces_radio_set = self.assert_component_exists(pilot, WORKSPACES_RADIO_SET_ID)
        workspaces = [str(button.label) for button in workspaces_radio_set.children]
        assert new in workspaces

        await pilot.hover(f"#id-{new}")
        await pilot.click(f"#id-{new}")
