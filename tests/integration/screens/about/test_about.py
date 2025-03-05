import pytest
from terraland.__version__ import __version__
from terraland.presentation.cli.screens.about.main import AboutScreen
from tests.integration.utils import click, DEFAULT_SCREEN_ID


class TestAboutScreen:
    """
    Feature: About screen
        As a user
        I want to see information about the application
        So that I can learn more about the application
    """

    ABOUT_CONTROLS_ID = "#about_controls"
    COPY_BUTTON_ID = "#copy"
    CLOSE_BUTTON_ID = "#close"
    HEADER_ID = "#header"
    ABOUT_BUTTON_ID = "#about"
    WINDOW_CONTENT_ID = "#window-content"

    @pytest.mark.asyncio
    async def test_about_screen(self, app):
        """
        Feature: View about screen
            Given the application is running
            When I click on the about button
            Then the about screen should be displayed
            And the screen should contain information about the application
        """
        async with app.run_test() as pilot:
            await self._navigate_to_about_screen(pilot)
            terraform_version = app.terraform_version
            screen_text = self._get_about_screen_text(pilot)
            self._verify_about_screen_content(terraform_version, screen_text)

    @pytest.mark.asyncio
    async def test_about_screen_copy_action(self, app):
        """
        Feature: Copy about screen content
            Given the application is running
            When I click on the about button
            And I click on the copy button
            Then the about screen content should be copied to the clipboard
        """
        async with app.run_test() as pilot:
            await self._navigate_to_about_screen(pilot)
            await self._click_button_in_controls(pilot, self.COPY_BUTTON_ID)
            terraform_version = app.terraform_version
            expected_clipboard_content = f"""
                TerraLand {__version__}
                Terraform version: {terraform_version.terraform_version}
                Platform: {terraform_version.platform}
                Powered by: the-impact-craft
                """
            assert pilot.app.clipboard == expected_clipboard_content

    @pytest.mark.asyncio
    async def test_about_screen_close_action(self, app):
        """
        Feature: Close about screen
            Given the application is running
            When I click on the about button
            And I click on the close button
            Then the about screen should be closed
            And the default screen should be displayed
        """
        async with app.run_test() as pilot:
            await self._navigate_to_about_screen(pilot)
            await self._click_button_in_controls(pilot, self.CLOSE_BUTTON_ID)
            assert pilot.app.screen.id == DEFAULT_SCREEN_ID

    @staticmethod
    async def _navigate_to_about_screen(pilot):
        """
        Navigate to the about screen.
        """
        header = pilot.app.query_one(TestAboutScreen.HEADER_ID)
        about_button = header.query_one(TestAboutScreen.ABOUT_BUTTON_ID)
        await click(pilot, about_button)
        assert isinstance(pilot.app.screen, AboutScreen)

    @staticmethod
    def _get_about_screen_text(pilot) -> str:
        """
        Get the concatenated text content from the about screen.
        """
        window_content = pilot.app.query_one(TestAboutScreen.WINDOW_CONTENT_ID)
        return " ".join([component.renderable for component in window_content.children])

    @staticmethod
    def _verify_about_screen_content(terraform_version, screen_text):
        """
        Verify that the content on the about screen matches the expected Terraform version and details.
        """
        assert all(
            [
                i in screen_text
                for i in [
                    f"Terraform version: {terraform_version.terraform_version}",
                    f"Platform: {terraform_version.platform}",
                    "Powered by: the-impact-craft",
                ]
            ]
        )

    @staticmethod
    async def _click_button_in_controls(pilot, button_id):
        """
        Click a button within the about controls section.
        """
        about_controls = pilot.app.query_one(TestAboutScreen.ABOUT_CONTROLS_ID)
        button = about_controls.query_one(button_id)
        await click(pilot, button)
