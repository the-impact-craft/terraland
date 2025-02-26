from typing import List

from dependency_injector.wiring import Provide
from textual import work
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import ListView, ListItem, Label, Static

from terry.presentation.cli.cache import TerryCache
from terry.presentation.cli.di_container import DiContainer
from terry.presentation.cli.screens.main.sidebars.base import BaseSidebar


class CommandItem(Horizontal):
    DEFAULT_CSS = """
    CommandItem {
        height: auto;
        padding: 0 1;
        margin-bottom: 1;
        
        
        & > .command {
            width: 90%;
            height: auto;
            & > Label { 
                width: 100%;
            }
            
            .timestamp {
                color: grey;
            }

        }
        & > .repeat_button {
            width: 10%;
        }
    }
    """

    def __init__(self, command: str, timestamp, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = command
        self.timestamp = timestamp

    def compose(self) -> ComposeResult:
        with Vertical(
            classes="command",
        ):
            yield Label(self.command)
            yield Static(self.timestamp, classes="timestamp")

        yield Static("⤾", classes="repeat_button").with_tooltip("Repeat command")


class CommandHistorySidebar(BaseSidebar):
    commands: reactive[List[dict]] = reactive([], recompose=True)

    def __init__(self, cache: TerryCache = Provide[DiContainer.cache], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = cache
        self.list_view = None

    def compose(self) -> ComposeResult:
        with ListView() as self.list_view:
            for command in reversed(self.commands):
                yield ListItem(CommandItem(command.get("command"), command.get("timestamp")))

    def toggle(self, visible: bool):
        self.set_class(visible, "-visible")
        if not self.list_view:
            return
        self.refresh_content()  # type: ignore
        self.list_view.focus()

    def on_mount(self, event):
        self.refresh_content()  # type: ignore

    @work(exclusive=True, thread=True)
    async def refresh_content(self):
        self.commands = self.cache.get("commands", [])  # type: ignore
