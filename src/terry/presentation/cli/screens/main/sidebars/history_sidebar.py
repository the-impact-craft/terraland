from textual.app import ComposeResult
from textual.widgets import ListView, ListItem, Label

from terry.presentation.cli.screens.main.sidebars.base import BaseSidebar


class CommandHistorySidebar(BaseSidebar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_view = None

    def compose(self) -> ComposeResult:
        with ListView() as self.list_view:
            yield ListItem(Label("terraform apply"))
            yield ListItem(Label("terraform validate"))
            yield ListItem(Label("terraform validate"))
            yield ListItem(Label("terraform format"))

    def toggle(self, visible: bool):
        self.set_class(visible, "-visible")
        if not self.list_view:
            return
        self.list_view.focus()
