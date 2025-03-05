import asyncio
import json
from pathlib import Path
from typing import Any
from uuid import uuid4

from dependency_injector.wiring import Provide
from rich.text import TextType
from textual import work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, Container
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import TextArea, Tree, Tabs, Tab, Static
from textual.widgets._tree import TreeNode

from terraland.infrastructure.file_system.services import FileSystemService
from terraland.logo import LOGO_ANIMATION
from terraland.presentation.cli.di_container import DiContainer
from terraland.presentation.cli.screens.main.containers.text_area_style import (
    terrafort_text_area_theme,
    TERRAFORT_THEME_NAME,
)
from terraland.settings import DEFAULT_LANGUAGE, ANIMATION_SPEED


class Preview(Horizontal):
    file_name: reactive[str | None] = reactive(None, recompose=False)
    content: reactive[str | None] = reactive(None, recompose=True)
    language: reactive[str] = reactive(DEFAULT_LANGUAGE, recompose=True)
    selected_line: reactive[int] = reactive(0, recompose=True)

    DEFAULT_CSS = """
    #no_content_label {
        width: 100%;
        align: center middle;
    }
    #no_content_label_content {
        width: auto;
        color: $secondary-background;
    }
    Tree {
        background: $background;
        &:focus {
            background-tint: $background;
        }
    }
    TextArea {
        background-tint: $background;
    }
    """

    BINDINGS = [Binding("ctrl+s", "save", "Save file")]

    def __init__(self, animation_enabled: bool = Provide[DiContainer.config.animation_enabled], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animation_task_running = None
        self.animation_enabled = animation_enabled
        self.text_area = None

    def compose(self) -> ComposeResult:
        """
        Compose the preview widget based on the content and language.

        This method generates the UI components for displaying the content preview. It handles different scenarios:

        - No content: Displays a "No content to display" label

        - Non-JSON/non-Terraform state files: Shows the content in a code editor with appropriate language

        - JSON/Terraform state files: Attempts to parse JSON and display content in a tabbed interface

        Returns:
            ComposeResult: A generator yielding Textual UI components for rendering
        """

        self.text_area = TextArea(
            self.content or "",
            language=self.language,
            show_line_numbers=True,
        )

        self.text_area.register_theme(terrafort_text_area_theme)
        self.text_area.theme = TERRAFORT_THEME_NAME

        if self.content is None:
            yield Container(
                Static(LOGO_ANIMATION[-1], id="no_content_label_content", markup=False),
                id="no_content_label",
            )
            yield self.text_area
            if self.animation_enabled and not self.animation_task_running:
                self.turn_animation_on()
            return

        self.turn_animation_off()
        if self.language in ["json"]:
            try:
                data = json.loads(self.content)
            except json.JSONDecodeError:
                yield self.text_area
                self.notify("Invalid JSON content.")
            else:
                with Horizontal(id="json-preview"):
                    yield self.text_area
                    yield self.build_tree(data)
        else:
            yield self.text_area
        if self.selected_line:
            self.text_area.cursor_location = (self.selected_line, 0)

    @work(exclusive=True, thread=True)
    async def animate_logo(self):
        """
        Asynchronously animates a logo in a GUI application. This function updates the text of
        a specified label widget with frames from a predefined animation sequence. The process
        continues until the content becomes available. The updates are performed at regular
        intervals configured by a global animation speed constant. The function utilizes
        coroutines and asynchronous tasks to ensure non-blocking execution.

        :param self: Reference to the current instance of the class.
        :return: None
        """
        frame_number = 0
        while self.animation_task_running:
            await asyncio.sleep(ANIMATION_SPEED)
            try:
                text_container: Static = self.query_one("#no_content_label_content")  # type: ignore
            except NoMatches:
                self.log.warning("Error updating logo animation.")
                return
            if text_container:
                text_container.update(LOGO_ANIMATION[frame_number % len(LOGO_ANIMATION)])
                frame_number += 1

    def turn_animation_on(self):
        """
        Turn on the logo animation.
        """
        self.animation_task_running = True
        self.animate_logo()

    def turn_animation_off(self):
        """
        Turn off the logo animation.
        """
        self.animation_task_running = False

    def build_tree(
        self,
        data: dict | list | TextType | Any,
        tree: Tree[str] | None = None,  # type: ignore
        node: TreeNode | None = None,
    ) -> Tree[str] | Widget:
        """
        Recursively build a tree representation of nested data structures.

        This method transforms dictionaries, lists, and other data types into a hierarchical tree structure, suitable
        for visualization. It supports nested dictionaries and lists, creating expandable nodes and leaf nodes
        accordingly.

        Parameters:
            data (dict | list | Any): The input data to be converted into a tree structure.
            tree (Tree[str], optional): The root tree object. Defaults to None.
            node (TreeNode, optional): The current node being processed. Defaults to None.

        Returns:
            Tree[str]: A fully constructed tree representation of the input data.

        Notes:
            - Dictionaries are converted with keys as nodes and simple values as leaves
            - Nested dictionaries and lists create expandable inner nodes
            - Primitive values are added as leaf nodes
            - The initial call automatically creates a root "State:" node
        """
        if node is None:
            tree: Tree[str] = Tree("State:", id="state-tree")
            tree.root.expand()
            node = tree.root

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    inner_node = node.add(key, expand=True)
                    self.build_tree(value, tree, inner_node)
                else:
                    node.add_leaf(f"{key}: {value}")
        elif isinstance(data, list):
            for item in data:
                self.build_tree(item, tree, node)
        else:
            node.add_leaf(data)
        if not tree:
            tree = Tree("State:", id="state-tree")
        return tree

    def reset(self):
        """
        Resets the content and language attributes of the instance to their default values.

        This method is used to clear the current content and reset the language
        to the predefined default language constant.
        """
        self.content = None
        self.file_name = None
        self.language = DEFAULT_LANGUAGE

    def action_save(self, file_system_service: FileSystemService = Provide[DiContainer.file_system_service]):
        """
        Saves the current content of the text area to a specified file using the provided
        file system service. This method will generate a temporary file path and save the
        content to the original file location through an intermediary temporary file.

        Arguments:
            file_system_service: The service instance responsible for handling file system operations, expected to be
            provided via dependency injection.

        """
        if self.text_area is None or self.file_name is None:
            return
        temp_file_name = self._generate_temp_file_path(file_system_service)
        original_file_name = file_system_service.work_dir / self.file_name
        content = self.text_area.document.text
        self.content = content
        # Todo: add cursor position

        self._save_content_to_file(file_system_service, temp_file_name, original_file_name, content)

    def _generate_temp_file_path(self, file_system_service: FileSystemService) -> Path:
        """
        Generates a unique temporary file path in the work directory of the provided
        file system service by appending a UUID to the file name.

        Arguments:
            file_system_service (FileSystemService): Service providing access to the file system,
            including the work directory.
        Returns:
            Path: A file path composed of the work directory, the initial file name,
            and a unique identifier.
        """
        return file_system_service.work_dir / f"{self.file_name}+{uuid4()}"

    @staticmethod
    def _save_content_to_file(
        file_system_service: FileSystemService, temp_path: Path, original_path: Path, content: str
    ) -> None:
        """
        This function saves the provided content to a file by first creating a file
        at the specified temporary path and then moving it to the original target
        path using a given file system service.

        Arguments:
            file_system_service (FileSystemService): The service used to manipulate file system operations.
            temp_path (Path): The temporary path where the file will be created before being moved to the original path.
            original_path (Path): The target path where the file will ultimately be saved after being moved.
            content (str): The string content to be saved into the file.
        """
        file_system_service.create_file(path=temp_path, content=content)
        file_system_service.move(src_path=temp_path, dest_path=original_path)


class Content(Vertical):
    """
    Widget for managing the content.
    """

    DEFAULT_CSS = """
     Content > TextArea {
        scrollbar-color: #097F5A;
        scrollbar-color-active: #097F5A;
        scrollbar-color-hover: #097F5A;
    }
    """

    BINDINGS = [
        ("r", "remove", "Remove active tab"),
        ("c", "clear", "Clear tabs"),
    ]

    can_focus = False

    # Todo: create lexer hcl language
    languages = {
        ".py": "python",
        ".tf": "python",
        ".json": "json",
        ".tfstate": "json",
    }

    def __init__(self, *args, **kwargs):
        """
        Initialize a new Content widget instance.

        Calls the parent Vertical container's initialization method with the provided arguments.

        Args:
            *args: Variable length argument list passed to the parent class constructor.
            **kwargs: Arbitrary keyword arguments passed to the parent class constructor.
        """
        super().__init__(*args, **kwargs)
        self.files_contents = {}
        self.active_tab = None

    def compose(self) -> ComposeResult:
        """
        Compose the widget's content based on the file type and content.

        This method generates the UI components for displaying file content. It handles different scenarios:
        - No content: Displays a "No content to display" label
        - Non-JSON/non-Terraform state files: Shows file path and code editor with appropriate language
        - JSON/Terraform state files: Attempts to parse JSON and display content in a tabbed interface

        Parameters:
            self (Content): The current Content widget instance

        Returns:
            ComposeResult: A generator yielding Textual UI components for rendering

        Raises:
            json.JSONDecodeError: If JSON parsing fails for JSON/Terraform state files
        """

        yield Tabs(id="tabbed-content")
        yield Preview(id="content-preview")

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """
        Handle the activation of a tab in the content widget.

        This method is triggered when a tab is activated in the Tabs component. It manages the visibility and content
        of the associated TextArea based on the selected tab.

        Parameters:
            event (Tabs.TabActivated): The event object representing the tab activation, containing information about
            the activated tab.

        Behavior:
            - If no tab is selected (event.tab is None), the TextArea is hidden.
            - If a tab is selected, the TextArea becomes visible and its content is updated from the files_contents
            dictionary.
            - Retrieves the content associated with the tab's label from the files_contents dictionary.
            - Defaults to an empty string if no content is found for the given tab.

        Side Effects:
            - Modifies the visibility of the TextArea widget.
            - Updates the text content of the TextArea.
        """
        text_area = self.query_one("#content-preview")
        preview = self.query_one(Preview)
        if event.tab is None:
            text_area.visible = False
        else:
            text_area.visible = True
            file_name = str(event.tab.label)
            self.active_tab = file_name
            preview.file_name = file_name
            preview.language = self.languages.get(Path(file_name).suffix, DEFAULT_LANGUAGE)
            preview.content = self.files_contents.get(file_name, {}).get("content", "")

    async def add(self, name, content, selected_line) -> None:
        """
        Add a new tab to the content view with the specified file name and content.

        This method handles tab creation, ensuring no duplicate tabs and maintaining a consistent UI state. If a tab
        for the file already exists, it activates that tab. Otherwise, it creates a new tab with a unique identifier.

        Parameters:
            name (str): The name of the file to be added as a tab label
            content (str): The text content to be displayed in the text area
            selected_line (int): The line number to highlight in the text area

        Side Effects:
            - Adds a new tab to the Tabs widget
            - Updates the TextArea with the file's content
            - Sets syntax highlighting based on file extension
            - Stores file information in the files_contents dictionary
            - Activates the newly created or existing tab

        Notes:
            - Uses UUID to generate unique tab identifiers
            - Defaults to Python syntax highlighting if file extension is not recognized
        """
        tabs = self.query_one(Tabs)
        if name in self.files_contents:
            preview = self.query_one(Preview)
            preview.selected_line = selected_line
            tabs.active = self.files_contents.get(name, {}).get("id", "")
            return

        active_tab = tabs.active_tab
        tab_id = "a" + str(uuid4())
        await tabs.add_tab(Tab(name, id=tab_id), after=active_tab.id if active_tab else None)

        self.files_contents[name] = {"content": content, "id": tab_id}

        preview = self.query_one(Preview)
        preview.file_name = name
        preview.language = self.languages.get(Path(name).suffix, "python")
        preview.content = content
        preview.selected_line = selected_line
        self.active_tab = name
        tabs.active = tab_id

    def update(self, name, content):
        """
        Updates the content of a given file if it exists in the internal dictionary
        of file contents. Also updates the content displayed in the active tab
        if its label matches the given file name.

        Arguments:
            name (str): The name of the file to update
            content (str): The new content to set for the file
        """
        if name not in self.files_contents:
            return

        tabs = self.query_one(Tabs)
        if not tabs.active_tab:
            return

        self.files_contents[name]["content"] = content
        active_label = str(tabs.active_tab.label)

        if active_label == name:
            preview = self.query_one(Preview)
            preview.file_name = name
            preview.content = content

    def activate(self, tab_number):
        tabs_container = self.query_one(Tabs)
        tabs = list(tabs_container.query("#tabs-list > Tab").results(Tab))
        if tab_number > len(tabs):
            return
        tabs_container.active = tabs[tab_number - 1].id

    def action_remove(self) -> None:
        """
        Remove the currently active tab from the content view.

        This method removes the active tab from the Tabs widget and deletes its corresponding content from the
        files_contents dictionary. If no tab is currently active, no action is taken.

        Side Effects:
            - Removes the active tab from the Tabs widget
            - Deletes the tab's content from the files_contents dictionary
            - Updates the UI to reflect the tab removal

        Raises:
            KeyError: If the tab's label is not found in files_contents
        """
        tabs = self.query_one(Tabs)
        active_tab = tabs.active_tab
        self.remove_tab(getattr(active_tab, "id", None), str(getattr(active_tab, "label", "")))

    def remove_tab(self, uuid, label):
        tabs = self.query_one(Tabs)
        if uuid is not None:
            tabs.remove_tab(uuid)
            del self.files_contents[label]
        if not self.files_contents:
            self.query_one(Preview).reset()
            self.active_tab = None

    def action_clear(self) -> None:
        """
        Clear all open tabs and reset the content display.

        This method performs the following actions:
        - Empties the `files_contents` dictionary, removing all stored file contents
        - Removes all tabs from the Tabs widget
        - Clears the text content of the TextArea

        No parameters are required, and no value is returned.
        """
        self.files_contents = {}
        self.query_one(Tabs).clear()
        self.query_one(Preview).reset()
        self.active_tab = None
