from unittest.mock import patch, MagicMock
import pytest
from terraland.presentation.cli.screens.tf_format.main import FormatSettingsScreen
from tests.integration.utils import DEFAULT_SCREEN_ID, click


class TestFormatScreen:
    """
    Feature: Format screen
        As a user
        I want to see format settings
        So that I can customize the format settings
    """

    # Constants for element IDs
    CONTROLS_ID = "#controls"
    CLOSE_BUTTON_ID = "#close"
    APPLY_BUTTON_ID = "#apply"
    HEADER_ID = "#header"
    FORMAT_BUTTON_ID = "#fmt"

    @pytest.mark.asyncio
    async def test_format_screen_displayed(self, app):
        """
        Feature: View format screen
            Given the application is running
            When I click on the format button
            Then the format screen should be displayed
            And the screen should contain format settings
        """
        async with app.run_test() as pilot:
            await self._open_format_window(pilot)
            self._assert_screen_is_format_settings(pilot)

    @pytest.mark.asyncio
    async def test_format_screen_close_action(self, app):
        """
        Feature: Close format screen
            Given the application is running
            When I open the format screen
            And I click on the close button
            Then the format screen should be closed
            And the default screen should be displayed
        """
        async with app.run_test() as pilot:
            await self._open_format_window(pilot)
            self._assert_screen_is_format_settings(pilot)

            close_button = self._get_button_by_id(pilot, self.CLOSE_BUTTON_ID)
            await click(pilot, close_button)

            assert pilot.app.screen.id == DEFAULT_SCREEN_ID

    @pytest.mark.asyncio
    async def test_format_screen_apply_action(self, app):
        """
        Feature: Apply format settings
            Given the application is running
            When I open the format screen
            And I click on the apply button
            Then the format settings action should be executed
        """

        handler_mock = MagicMock()
        async with app.run_test() as pilot:
            await pilot.app.push_screen(FormatSettingsScreen(), callback=handler_mock)
            self._assert_screen_is_format_settings(pilot)

            apply_button = self._get_button_by_id(pilot, self.APPLY_BUTTON_ID)
            await click(pilot, apply_button)
            handler_mock.assert_called_once()
            assert pilot.app.screen.id == DEFAULT_SCREEN_ID

    @staticmethod
    async def _open_format_window(pilot):
        """
        Open the format window.
        Arguments:
            pilot (Pilot): The Pilot test instance.
        """
        header = pilot.app.query_one(TestFormatScreen.HEADER_ID)
        format_button = header.query_one(TestFormatScreen.FORMAT_BUTTON_ID)
        format_button.scroll_visible()
        await click(pilot, format_button)

    @staticmethod
    def _get_button_by_id(pilot, button_id):
        """
        Retrieve a button component by its ID within the controls.
        Arguments:
            pilot (Pilot): The Pilot test instance.
            button_id (str): The ID of the button to query.
        Returns:
            Button: The found button instance.
        """

        controls = pilot.app.query_one(TestFormatScreen.CONTROLS_ID)
        return controls.query_one(button_id)

    @staticmethod
    def _assert_screen_is_format_settings(pilot):
        """
        Assert that the current screen is the FormatSettingsScreen.
        Arguments:
            pilot (Pilot): The Pilot test instance.
        """
        assert isinstance(pilot.app.screen, FormatSettingsScreen)
