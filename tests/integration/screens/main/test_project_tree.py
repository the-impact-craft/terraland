import pytest
from textual.widgets import DirectoryTree

from terraland.presentation.cli.screens.main.containers.project_tree import TfDirectoryTree


class TestProjectTree:
    """
    Feature: Project File Navigation
    As a user
    I want to browse project files
    So that I can access Terraform configurations
    """

    @staticmethod
    def get_file_nodes_from_tree(directory_tree):
        """
        Extract all file nodes (non-folder items) from a directory tree.

        Parameters:
            directory_tree (DirectoryTree): The directory tree widget.

        Returns:
            list: A list of file nodes extracted from the directory tree.
        """
        return [node for node in directory_tree.root.children if not directory_tree._safe_is_dir(node.data.path)]

    @pytest.mark.asyncio
    async def test_project_tree_initialization(self, app, tmp_path):
        """
        Scenario: Initialize project tree component
            Given the project tree component is mounted
            Then the component should have a "Project tree" border title
            And a DirectoryTree widget should be present
            And it should display the project root directory
        """
        async with app.run_test() as pilot:
            project_tree = pilot.app.query_one("#project_tree")
            directory_tree = project_tree.query_one(TfDirectoryTree)

            assert project_tree.border_title == "Project tree"
            assert directory_tree is not None
            assert directory_tree.path == pilot.app.work_dir

    @pytest.mark.asyncio
    async def test_file_selection(self, app, tmp_path):
        """
        Scenario: Select Terraform files
            Given the project tree is mounted
            And Terraform files exist in the project
            When I click on a Terraform file
            Then a FileSelect event should be posted
            And the file should be highlighted
        """
        # Setup: Create a Terraform file in the temporary test path
        file_path = tmp_path / "main.tf"
        file_path.touch()
        app.file_system_service.read.return_value = "resource 'aws_instance' 'example' {}"

        async with app.run_test() as pilot:
            # Locate components
            project_tree = pilot.app.query_one("#project_tree")
            directory_tree = project_tree.query_one(DirectoryTree)
            main_content_container = pilot.app.query_one("#content")
            tabbed_content_view = main_content_container.query_one("#tabbed-content")

            # Extract file nodes from the directory tree
            file_nodes = self.get_file_nodes_from_tree(directory_tree)
            assert len(file_nodes) == 1

            # Simulate double-clicking the file node
            for _ in range(2):
                directory_tree.select_node(file_nodes[0])
            await pilot.pause()

            # Assertions
            assert str(file_nodes[0].label) == str(tabbed_content_view.active_tab.label)
