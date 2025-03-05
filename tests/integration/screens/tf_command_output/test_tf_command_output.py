import pytest
from io import StringIO
from textual.widgets import Input
from terraland.presentation.cli.screens.tf_command_output.main import CommandOutputComponent, TerraformCommandOutputScreen


class TestTerraformCommandOutputScreen:
    @pytest.mark.asyncio
    async def test_screen_creation(self, app):
        """
        Scenario: Test TerraformCommandOutputScreen creation
        Given the TerraformCommandOutputScreen
        When the screen is mounted
        Then the screen should contain a command output component
        """

        screen = TerraformCommandOutputScreen()
        async with app.run_test() as pilot:
            await pilot.app.push_screen(screen)

            # Verify components
            assert screen.query_one(CommandOutputComponent) is not None
            assert screen.query_one(Input) is not None
            assert screen.query_one(f"#{screen.CONTAINER_ID}") is not None

    @pytest.mark.asyncio
    async def test_log_writing(self, app):
        """
        Scenario: Test writing log messages
        Given the TerraformCommandOutputScreen
        When I write log messages
        Then the log messages should be displayed
        """

        screen = TerraformCommandOutputScreen()
        async with app.run_test() as pilot:
            await pilot.app.push_screen(screen)

            # Write log messages
            screen.write_log("First message")
            screen.write_log("Second message")
            await pilot.pause()

            # Verify log content
            command_output = screen.query_one(CommandOutputComponent)
            assert "First message" in command_output.log_content
            assert "Second message" in command_output.log_content

    @pytest.mark.asyncio
    async def test_input_handling(self, app):
        """Test input handling with stdin"""

        screen = TerraformCommandOutputScreen()
        stdin = StringIO()
        async with app.run_test() as pilot:
            await pilot.app.push_screen(screen)

            # Set stdin and write a prompt
            screen.stdin = stdin
            screen.write_log("Enter a value:")
            await pilot.pause()

            # Verify input area is focused
            input_area = screen.query_one(Input)
            assert input_area.has_focus

            # Submit input
            await pilot.press("h", "e", "l", "l", "o", "enter")
            await pilot.pause()

            # Verify input is processed
            command_output = screen.query_one(CommandOutputComponent)
            assert "Enter a value: hello" in command_output.log_content
            assert stdin.getvalue() == "hello\n"

    @pytest.mark.asyncio
    async def test_input_area_disabled_without_stdin(self, app):
        """Test input area is disabled when stdin is not available"""

        screen = TerraformCommandOutputScreen()
        async with app.run_test() as pilot:
            await pilot.app.push_screen(screen)

            # Verify input area is disabled by default
            input_area = screen.query_one(Input)
            assert input_area.disabled

            # Set stdin and verify input area is enabled
            screen.stdin = StringIO()
            await pilot.pause()
            assert not input_area.disabled

    @pytest.mark.asyncio
    async def test_screen_closing(self, app):
        """Test screen closing functionality"""

        screen = TerraformCommandOutputScreen()
        async with app.run_test() as pilot:
            await pilot.app.push_screen(screen)

            # Test escape key
            await pilot.press("escape")
            assert pilot.app.screen is not screen

    @pytest.mark.asyncio
    async def test_input_focus_management(self, app):
        """Test input focus management"""

        screen = TerraformCommandOutputScreen()
        stdin = StringIO()
        async with app.run_test() as pilot:
            await pilot.app.push_screen(screen)
            screen.stdin = stdin

            # Write prompt and verify focus
            screen.write_log("Enter a value:")
            await pilot.pause()
            input_area = screen.query_one(Input)
            assert input_area.has_focus

            # Submit input and verify focus is removed
            await pilot.press("t", "e", "s", "t", "enter")
            await pilot.pause()
            assert not input_area.has_focus

    @pytest.mark.asyncio
    async def test_multiple_inputs(self, app):
        """Test handling multiple input prompts"""

        screen = TerraformCommandOutputScreen()
        stdin = StringIO()
        async with app.run_test() as pilot:
            await pilot.app.push_screen(screen)
            screen.stdin = stdin

            # First input
            screen.write_log("Enter a value:")
            await pilot.pause()
            await pilot.press("o", "n", "e", "enter")
            await pilot.pause()

            # Second input
            screen.write_log("Enter a value:")
            await pilot.pause()
            await pilot.press("t", "w", "o", "enter")
            await pilot.pause()

            # Verify both inputs are processed
            command_output = screen.query_one(CommandOutputComponent)
            assert "Enter a value: one" in command_output.log_content
            assert "Enter a value: two" in command_output.log_content
