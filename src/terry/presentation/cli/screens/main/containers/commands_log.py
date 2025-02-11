from rich.highlighter import JSONHighlighter
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import RichLog


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

    def __init__(self, content, *args, **kwargs):
        """
        Initialize a new CommandsLog widget with the given content.

        Parameters:
            content (Any): The content to be associated with the CommandsLog widget
            *args: Variable positional arguments passed to the parent VerticalScroll constructor
            **kwargs: Variable keyword arguments passed to the parent VerticalScroll constructor

        Attributes:
            content (Any): Stores the provided content for potential later use in the widget
        """
        self.content = content
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        """
        Compose the user interface for the CommandsLog widget.

        Yields a RichLog component with a predefined ID and markup enabled, which will display the command execution
        logs.

        Returns:
            ComposeResult: A generator yielding the RichLog widget for rendering
        """

        rich_log = RichLog(id=self.LOG_COMPONENT_ID, markup=True, highlight=True)
        rich_log.highlighter = JSONHighlighter()
        yield rich_log

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
