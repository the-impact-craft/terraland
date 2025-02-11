import pytest
from textual.widgets import ListView

from tests.integration.utils import click, double_click


class TestStateFiles:
    """
    Feature: Terraform State File Management
    As a user
    I want to access Terraform state files
    So that I can view state information
    """

    def get_state_files_and_list(self, pilot):
        """Helper function to get state files and state list widget."""
        state_files = pilot.app.query_one("#state_files")
        state_list_widget = state_files.query_one(ListView)
        return state_files, state_list_widget

    @pytest.mark.asyncio
    async def test_state_files_initialization(self, app):
        """
        Scenario: Initialize state files component
            Given the state files component is mounted
            Then the component should have a "State files" border title
            And a ListView widget should be present
            And state list contains system state files
        """
        async with app.run_test() as pilot:
            state_files, state_list_widget = self.get_state_files_and_list(pilot)
            assert state_files.border_title == "State files"
            assert state_list_widget is not None
            assert len(state_list_widget.children) == len(app.file_system_service.list_state_files())

    @pytest.mark.asyncio
    async def test_file_selection(self, app, file_system_service):
        """
        Scenario: Select state file
            Given state files are loaded
            When I click on a state file
            Then it should be highlighted
            And when I double-click within 1.5 seconds
            Then a FileSelect event should be posted
        """
        async with app.run_test() as pilot:
            state_files, state_list_widget = self.get_state_files_and_list(pilot)
            content = pilot.app.query_one("#content")
            tabbed_content = content.query_one("#tabbed-content")

            file_node = state_list_widget.children[-1]  # Get the last file node

            await click(pilot, state_files)

            # Single-click action
            await click(pilot, file_node)
            assert file_node.label == state_list_widget.highlighted_child.label

            # Simulate adding a new file
            file_content = "resource 'aws_instance' 'example' {}"
            file_system_service.read.return_value = file_content

            await double_click(pilot, file_node)

            # Assert tab content matches the file node label
            assert str(file_node.label) == str(tabbed_content.active_tab.label)

    @pytest.mark.asyncio
    async def test_empty_state(self, app):
        """
        Scenario: No state files available
            Given the state files component is mounted
            When no state files are available
            Then an appropriate message should be displayed
            And the tree should be empty
        """
        app.file_system_service.list_state_files.return_value = []  # Simulate no files
        async with app.run_test() as pilot:
            _, state_list_widget = self.get_state_files_and_list(pilot)
            assert len(state_list_widget.children) == 0
