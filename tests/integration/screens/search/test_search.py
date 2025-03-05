import pytest

from terraland.presentation.cli.screens.search.main import SearchScreen

# Constants for maintainability
SEARCH_KEY_BINDING = "ctrl+f"
EXPECTED_SCREEN_TYPE = SearchScreen


class TestSearchScreen:  # Renamed class for accuracy
    @pytest.mark.asyncio
    async def test_search_screen(self, app):
        async with app.run_test() as pilot:
            # Trigger the search screen
            await pilot.press(SEARCH_KEY_BINDING)

            # Allow some time for the screen to load
            await pilot.pause()

            # Assert the type of the screen is as expected
            assert isinstance(pilot.app.screen, EXPECTED_SCREEN_TYPE)
