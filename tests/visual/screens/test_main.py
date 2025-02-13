#
# def test_main_screen(app, snap_compare):
#     """
#     Tests the main screen of the application by comparing its current state
#     to a predefined snapshot. This ensures that the main screen layout
#     and functionality remain consistent over time.
#     """
#     assert snap_compare(app)
#
#
# def test_switch_workspace(app, snap_compare):
#     """
#     Tests the functionality to switch workspaces within an application. It ensures
#     that the workspace switching operation works correctly and matches the expected
#     snapshot comparison.
#     """
#
#     async def run_before(pilot) -> None:
#         await pilot.hover("#workspaces")
#         await pilot.click("#id-default")
#
#     assert snap_compare(app, run_before=run_before)
#
# def test_open_tab(app, snap_compare):
#     """
#     Tests the functionality to open tabs within the application. It ensures
#     that the tab opening operation works correctly and matches the expected
#     snapshot comparison.
#     """
#
#     async def run_before(pilot) -> None:
#         content = pilot.app.query_one("#content")
#         tabbed_content = content.query_one('#tabbed-content')
#
#         # Add a file first
#         file_path = Path("main.tf")
#         file_content = "resource 'aws_instance' 'example' {}"
#         pilot.app.file_system_service.read.return_value = file_content
#         await pilot.app.on_file_select(FileSelect(file_path))
#
#         # Assert tab has been added
#         assert tabbed_content.tab_count == 1
#
#         # Activate the tab component
#         await pilot.hover(content)
#         await pilot.click(content)
#
#     assert snap_compare(app, run_before=run_before)
#
# def test_about_screen(app, snap_compare):
#     """
#     Tests the about screen of the application by comparing its current state
#     to a predefined snapshot. This ensures that the about screen layout
#     and functionality remain consistent over time.
#     """
#
#     async def run_before(pilot) -> None:
#         header = pilot.app.query_one("#header")
#         about_button = header.query_one("#about")
#         about_button.scroll_visible()
#
#         await pilot.hover(about_button)
#         await pilot.click(about_button)
#
#         await pilot.pause(2)
#
#     assert snap_compare(app, run_before=run_before)
#
