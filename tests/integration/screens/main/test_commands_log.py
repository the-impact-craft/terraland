import pytest
from textual.widgets import RichLog

from terraland.settings import CommandStatus


class TestCommandsLog:
    """
    Feature: Command Execution Log Display
    As a user
    I want to see the command execution history
    So that I can track Terraform operations
    """

    BORDER_TITLE = "Commands log"
    LOG_COMPONENT_ID = "commands_log_component"

    def _get_log_widgets(self, app):
        """
        Helper to get main log and RichLog widgets.
        """
        commands_log = app.query_one("#commands_log")
        log_widget = commands_log.query_one(RichLog)
        return commands_log, log_widget

    def _extract_log_output(self, log_widget):
        """
        Extract and return the concatenated log content from the widget.
        """
        return "\n".join([segment.text for line in log_widget.lines for segment in line._segments])

    @pytest.mark.asyncio
    async def test_log_initialization(self, app):
        """
        Scenario: Initialize command log component
            Given the command log component is mounted
            Then the component should have a "Commands log" border title
            And a RichLog widget should be present with the correct ID
            And the RichLog widget should have JSON highlighting enabled
        """
        async with app.run_test() as pilot:
            commands_log, log_widget = self._get_log_widgets(pilot.app)

            assert commands_log.border_title == self.BORDER_TITLE
            assert log_widget.id == self.LOG_COMPONENT_ID
            assert log_widget.markup is True
            assert log_widget.highlight is True

    @pytest.mark.asyncio
    async def test_log_entry_display(self, app):
        """
        Scenario: Display command execution log entries
            Given the command log component is mounted
            When a new command execution is logged
            Then the log entry should be displayed with correct formatting
            And it should include command text, timestamp, and status
        """
        async with app.run_test() as pilot:
            _, log_widget = self._get_log_widgets(pilot.app)

            # Write a test log entry
            command = "terraform init"
            details = "Initialization complete!"
            pilot.app.write_command_log(
                message=command,
                status=CommandStatus.SUCCESS,
                details=details,
            )

            # Verify log content
            log_content = self._extract_log_output(log_widget)
            assert command in log_content
            assert "🟢" in log_content  # Success icon
            assert details in log_content

    @pytest.mark.asyncio
    async def test_error_log_entry(self, app):
        """
        Scenario: Display error log entries
            Given the command log component is mounted
            When a command execution fails
            Then the log entry should be displayed with error formatting
            And it should include error status and details
        """
        async with app.run_test() as pilot:
            _, log_widget = self._get_log_widgets(pilot.app)

            # Write an error log entry
            command = "terraform apply"
            details = "Failed to apply changes"
            pilot.app.write_command_log(
                message=command,
                status=CommandStatus.ERROR,
                details=details,
            )

            # Verify log content
            log_content = self._extract_log_output(log_widget)
            assert command in log_content
            assert "🔴" in log_content  # Error icon
            assert details in log_content

    @pytest.mark.asyncio
    async def test_log_entry_with_no_details(self, app):
        """
        Scenario: Display command execution log entries
            Given the command log component is mounted
            When a new command execution is logged without details
            Then the log entry should be displayed with correct formatting
            And it should include command text, timestamp, and status
        """
        async with app.run_test() as pilot:
            _, log_widget = self._get_log_widgets(pilot.app)

            # Write an error log entry
            command = "terraform apply"
            pilot.app.write_command_log(
                message=command,
                status=CommandStatus.ERROR,
            )

            # Verify log content
            log_content = self._extract_log_output(log_widget)
            assert command in log_content
            assert "🔴" in log_content
