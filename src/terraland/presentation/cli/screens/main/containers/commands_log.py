from datetime import datetime

from rich.highlighter import JSONHighlighter
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import RichLog

from terraland.settings import STATUS_TO_ICON, CommandStatus


class CommandsLog(VerticalScroll):
    """
    Widget for managing the content.
    """

    DEFAULT_CSS = """
    CommandsLog > RichLog {
        background: transparent;
    }
    """

    LOG_COMPONENT_ID = "commands_log_component"

    def __init__(self, *args, **kwargs):
        """
        Initialize a new CommandsLog widget with the given content.

        Parameters:
            content (Any): The content to be associated with the CommandsLog widget
            *args: Variable positional arguments passed to the parent VerticalScroll constructor
            **kwargs: Variable keyword arguments passed to the parent VerticalScroll constructor

        Attributes:
            content (Any): Stores the provided content for potential later use in the widget
        """
        self.rich_log = None
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        """
        Compose the user interface for the CommandsLog widget.

        Yields a RichLog component with a predefined ID and markup enabled, which will display the command execution
        logs.

        Returns:
            ComposeResult: A generator yielding the RichLog widget for rendering
        """

        self.rich_log = RichLog(id=self.LOG_COMPONENT_ID, markup=True, highlight=True)
        self.rich_log.highlighter = JSONHighlighter()
        yield self.rich_log

    def on_mount(self) -> None:
        """
        Mount event handler for the CommandsLog widget.

        Sets the border title to "Commands log" and populates the log with ten alternating entries of successful and
        failed command executions. Each log entry includes a status emoji, timestamp, and a status message.

        This method is automatically called when the widget is mounted, providing initial sample log content to
        demonstrate the log's functionality.

        Notes:
            - Writes 10 log entries (5 successful, 5 failed)
            - Uses current datetime for timestamps
            - Utilizes status emojis (✅ for success, ❌ for failure)
        """
        self.border_title = "Commands log"

    def write(self, message: str) -> None:
        """
        Write a message to the log.

        Arguments:
            message (str): The message to write to the log
        """
        if not self.rich_log:
            return
        self.rich_log.write(message)

    def write_primary_message(self, message: str):
        """
        Writes a primary formatted message to the interface. The message is formatted
        with bold styling to highlight primary information for the user.

        Arguments:
            message (str): The message to write to the interface.
        """
        self.write(f"~$: [bold]{message}[/bold]")

    def write_secondary_message(self, message: str):
        """
        Writes a secondary message in a specific formatted style, typically used
        for displaying less emphasized text or informational content.

        Arguments:
            message (str): The message to write to the interface.
        """
        self.write(f"[#808080]{message}[/#808080]")

    def write_datetime_status_message(self, message: str, status: CommandStatus):
        """
        Writes a formatted status message that includes a timestamp, a corresponding
        status icon, and the message with the status name.

        The method uses the status provided to determine the appropriate icon from
        `STATUS_TO_ICON`. It then constructs a message format that incorporates the
        current datetime, the message provided, and the name of the status, styled
        according to specific formatting preferences.

        Arguments:
            message (str): The message to write to the interface.
            status (CommandStatus): The status of the command execution.
        """
        self.write(f"{STATUS_TO_ICON.get(status)} [#808080]{datetime.now()} {message} [/#808080][{status.name}]")
