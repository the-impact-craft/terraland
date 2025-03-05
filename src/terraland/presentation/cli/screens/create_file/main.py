from dataclasses import dataclass
from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Label, Input

from terraland.infrastructure.file_system.exceptions import CreateFileException, CreateDirException
from terraland.presentation.cli.widgets.modal_control_label import ModalControlLabel


class Control(ModalControlLabel):
    """
    A clickable label that emits an event when clicked.
    """

    @dataclass
    class NewFile(Message):
        pass

    @dataclass
    class NewDir(Message):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions_messages = {"file": self.NewFile, "dir": self.NewDir}


class FileInputModal(ModalScreen):
    """
    Screen for creating a new file.
    """

    CSS_PATH = "styles.tcss"
    CONTAINER_ID = "file_input_screen"
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Pop screen"),
    ]

    def __init__(self, title, default_dir: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.default_dir = default_dir
        self.input = None

    def compose(self) -> ComposeResult:
        self.input = Input(value=f"{self.default_dir}/", name="name", classes="input", id="name", select_on_focus=False)
        with Container(id=self.CONTAINER_ID):
            yield Label(self.title, classes="header")  # type: ignore
            yield self.input

    def on_input_submitted(self, _: Input.Submitted) -> None:
        self.dismiss(self.input.value)  # type: ignore


class CreateFileScreen(ModalScreen):
    """
    A screen for creating a new file or directory within a specified root directory.

    Attributes:
        file_system_service: The service used to interact with the file system.
        root_dir (Path): The root directory where the new file or directory will be created.
        default_dir (Path): The default directory path to be used in the input modal.
    """

    CSS_PATH = "styles.tcss"
    CONTAINER_ID = "new_file_screen"
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Pop screen"),
    ]

    def __init__(self, file_system_service, root_dir: Path, default_dir: Path, *args, **kwargs):
        """
        Initializes the CreateFileScreen with the given file system service, root directory, and default directory.

        Args:
            file_system_service: The service used to interact with the file system.
            root_dir (Path): The root directory where the new file or directory will be created.
            default_dir (Path): The default directory path to be used in the input modal.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.file_system_service = file_system_service
        self.root_dir = root_dir
        self.default_dir = default_dir

    def compose(self) -> ComposeResult:
        """
        Composes the UI elements for the screen.

        Returns:
            ComposeResult: The result of the composition containing the UI elements.
        """
        with Container(id=self.CONTAINER_ID):
            with Horizontal(id="controls"):
                yield Control("File", name="file", classes="button", id="file")
                yield Control("Directory", name="dir", classes="button", id="dir")

    def create_file(self, name: str):
        """
        Creates a new file with the given name in the root directory.

        Args:
            name (str): The name of the new file.
        """
        try:
            self.file_system_service.create_file(self.root_dir / name)
        except CreateFileException as e:
            self.notify(f"Unable to create file '{name}': {e}", severity="error")
        else:
            self.app.pop_screen()

    def create_dir(self, name: str):
        """
        Creates a new directory with the given name in the root directory.

        Args:
            name (str): The name of the new directory.
        """
        try:
            self.file_system_service.create_dir(self.root_dir / name)
        except CreateDirException as e:
            self.notify(f"Error creating directory '{name}': {e}", severity="error")
        else:
            self.app.pop_screen()

    def on_control_new_file(self, _: Control.NewFile) -> None:
        """
        Handles the event when the 'New File' control is activated.

        Args:
            _: The event object (not used).
        """
        self.app.push_screen(
            FileInputModal(default_dir=self.default_dir, title="New File"),
            self.create_file,  # type: ignore
        )

    def on_control_new_dir(self, _: Control.NewDir) -> None:
        """
        Handles the event when the 'New Directory' control is activated.

        Args:
            _: The event object (not used).
        """
        self.app.push_screen(
            FileInputModal(default_dir=self.default_dir, title="New Directory"),
            self.create_dir,  # type: ignore
        )
