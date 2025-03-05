from asyncio.tasks import sleep, create_task
from dataclasses import dataclass
from pathlib import Path
from time import time
from typing import List

from dependency_injector.wiring import Provide, inject
from textual import work
from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Input, Label, ListView, ListItem, Static, LoadingIndicator

from terraland.domain.file_system.entities import SearchResult
from terraland.infrastructure.file_system.exceptions import FileSystemGrepException
from terraland.infrastructure.file_system.services import FileSystemService
from terraland.presentation.cli.messages.files_select_message import FileSelect
from terraland.presentation.cli.di_container import DiContainer
from terraland.settings import MAX_RESULTS, MAX_TEXT_LENGTH, DOUBLE_CLICK_THRESHOLD


@dataclass
class Click:
    timestamp: float
    label: str


class ResultLine(ListItem):
    
    def __init__(self, search_result: SearchResult, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_result = search_result
    
    def compose(self) -> ComposeResult:
        search_line = f"{self.search_result.file_name}:{self.search_result.line}"
        with Horizontal(classes="search_result_item"):
            yield Static(self.search_result.text, classes="search_result_item_text", markup=False)
            yield Static(search_line, classes="search_result_item_path", name=search_line, markup=False)
    

class ResultComponent(Widget):
    RESULT_FILES_LIST_COMPONENT_ID = "search_result_list"
    
    search_result: reactive[List[SearchResult] | None] = reactive([], recompose=True)
    total_search_result: reactive[int] = reactive(0, recompose=True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_file_click = Click(time(), "")

    def compose(self) -> ComposeResult:
        """
        Compose the search results list view dynamically based on the current search results.

        This method generates a `ListView` containing `ListItem` widgets for each search result. Each list item is a
        horizontal layout displaying the result text and its corresponding file path.

        Returns:
            ComposeResult: A list view of search results with text and path for each item.

        Attributes:
            self.search_result (list): A list of tuples containing search result text and file path.
        """
        if not self.search_result:
            yield LoadingIndicator() if self.search_result is None else Label(
                "No results found.", variant="secondary", id="search_result_empty"
            )
            return

        yield ListView(
            *(ResultLine(item) for item in self.search_result),
            id=self.RESULT_FILES_LIST_COMPONENT_ID,
        )
        yield Label(
            f"Found {self.total_search_result} results. Shown top {min(20, self.total_search_result)} results",
            variant="secondary",
            classes="search_result_total",
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """
        Handle selection events in the state files list view, detecting double-click interactions.

        This method is triggered when an item in the list view is selected. It checks if the selected item is from the
        state files list and implements a double-click detection mechanism by comparing the time and label of
        consecutive clicks.

        Parameters:
            event (ListView.Selected): The selection event containing details about the selected list item.

        Side Effects:
            - Updates `self.last_file_click` with the current click's timestamp and label.
            - Posts a `FileSelect` if a double-click is detected within 1.5 seconds on the same item.

        Behavior:
            - Verifies the selection is from the state files list component.
            - Detects double-clicks by checking:
                1. Time between clicks is less than 1.5 seconds
                2. The same list item is clicked twice
            - Triggers a file double-click event when conditions are met.
        """
        try:
            label = event.item.query_one(".search_result_item_path").name
            if not label or ":" not in label:
                raise ValueError("Invalid format: missing name or line number")
            path, line_str = label.split(":", 1)
            line = int(line_str)
        except (ValueError, TypeError) as e:
            self.notify(f"Invalid search result format: {str(e)}", severity="error")
            return

        if event.list_view.id == self.RESULT_FILES_LIST_COMPONENT_ID:
            current_click = Click(time(), label)
            if self._is_double_click(current_click):
                self.post_message(FileSelect(Path(path), line - 1))
                self.app.pop_screen()

            self.last_file_click = current_click

    def _is_double_click(self, current_click: Click) -> bool:
        """Check if the current click constitutes a double-click."""
        return (
            current_click.timestamp - self.last_file_click.timestamp < DOUBLE_CLICK_THRESHOLD
            and current_click.label == self.last_file_click.label
        )


# class SearchScreen(ModalScreen):
class SearchScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    CSS_PATH = "styles.tcss"

    @inject
    def __init__(
        self,
        work_dir,
        file_system_service: FileSystemService = Provide[DiContainer.file_system_service],
        *args,
        **kwargs,
    ):
        """
        Initialize a SearchScreen instance for file searching.

        Parameters:
            work_dir (Path): The directory path where file searches will be performed
            file_system_service (FileSystemService): The file system service to use for search operations
            *args: Variable positional arguments passed to the parent class constructor
            **kwargs: Variable keyword arguments passed to the parent class constructor

        Attributes:
            work_dir (str): Stores the working directory for search operations
            search (str): Stores the current search query string
        """
        super().__init__(*args, **kwargs)
        self.work_dir = work_dir
        self.file_system_service = file_system_service

        self.search = ""
        self._search_task = None
        self._debounce_delay = 0.3  # 300ms delay

    def compose(self) -> ComposeResult:
        """
        Compose the search screen layout with a search input and results component.

        This method sets up the user interface for the search functionality by:
        - Creating a container with a title label
        - Adding an input field for search queries
        - Yielding a ResultComponent to display search results

        Returns:
            ComposeResult: A composition of UI widgets for the search screen
        """
        yield Container(
            Label("Find in files"),
            Input(placeholder="Search for something...", id="search_input"),
            id="search_container",
        )
        yield ResultComponent(id="search_result")

    @work(exclusive=True, thread=True)
    async def update_search_area(self, search_value: str) -> None:
        """
        Processes and formats the search results, limiting to the first 10 matches and truncating result text to 100
        characters.

        Parameters:
            search_value (str): The input change event containing the current search query value.

        Side Effects:
            - Updates the `search_result` of the `ResultComponent` with formatted search results.

        """
        result_component = self.query_one(ResultComponent)

        try:
            search_result = self.file_system_service.grep(search_value, MAX_RESULTS, MAX_TEXT_LENGTH)
        except FileSystemGrepException as e:
            self.notify(f"Search failed: {str(e)}", severity="error")
            result_component.search_result = []
            return
        if search_result.pattern != search_value:
            return

        if self.search == search_value:
            result_component.search_result = search_result.output
            result_component.total_search_result = search_result.total

    async def _debounced_search(self, value: str) -> None:
        """
        Debounces the search input to prevent rapid search queries.

        This method waits for a short delay before updating the search area with the input value.

        Parameters:
            value (str): The search query value to debounce

        Side Effects:
            - Calls the `update_search_area` method with the provided search query value
        """

        await sleep(self._debounce_delay)
        self.update_search_area(value)

    def on_input_changed(self, changed: Input.Changed) -> None:
        """
        Handle changes in the search input field by performing a grep search and updating the search results.

        Performs a search in the specified working directory using the input value.

        Parameters:
            changed (Input.Changed): The input change event containing the current search query value.

        Side Effects:
            - Updates the `search_result` of the `ResultComponent` with formatted search results.
        """
        self.search = changed.value
        result_component = self.query_one(ResultComponent)

        if not self.search:
            result_component.search_result = []
            return

        result_component.search_result = None

        if self._search_task:
            self._search_task.cancel()

        self._search_task = create_task(self._debounced_search(self.search))
