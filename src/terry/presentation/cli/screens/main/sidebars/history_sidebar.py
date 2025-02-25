from typing import List

from dependency_injector.wiring import Provide
from textual import work
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import ListView, ListItem, Label

from terry.presentation.cli.cache import TerryCache
from terry.presentation.cli.di_container import DiContainer
from terry.presentation.cli.screens.main.sidebars.base import BaseSidebar


class CommandHistorySidebar(BaseSidebar):
    commands: reactive[List[str]] = reactive([], recompose=True)

    def __init__(self, cache: TerryCache = Provide[DiContainer.cache], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = cache
        self.list_view = None

    def compose(self) -> ComposeResult:
        with ListView() as self.list_view:
            for command in reversed(self.commands):
                yield ListItem(Label(command))

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
