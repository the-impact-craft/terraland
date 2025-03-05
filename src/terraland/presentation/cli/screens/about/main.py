from dataclasses import dataclass

from textual import events
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Label, Static

from terraland.__version__ import __version__


class ModalControlLabel(Label):
    """A clickable label that emits an event when clicked."""

    DEFAULT_CSS = """
    ModalControlLabel {
        margin: 0 4;
        padding: 0 0;
        width: auto;
        min-width: 16;
        height: auto;
        color: white;
        background: $surface;
        border: solid $surface-lighten-1;
        text-align: center;
        content-align: center middle;
        text-style: bold;

        &:disabled {
            text-opacity: 0.6;
        }

        &:focus {
            background-tint: $foreground 5%;
        }
        &:hover {
            border-top: solid $surface;
            background: $surface-darken-1;
        }
        &.-active {
            background: $surface;
            border-bottom: solid $surface-darken-1;
            tint: $background 30%;
        }
    }
    """
    can_focus = False

    @dataclass
    class ClickEvent(Message):
        """
        Posted when a workspace is changed.

        Can be handled using `on_clickable_label_click_event`.
        """

        action: str

    def __init__(self, *args, **kwargs):
        """
        Initialize a ClickableLabel widget.

        Parameters:
            *args: Variable length argument list passed to the parent class constructor.
            **kwargs: Arbitrary keyword arguments passed to the parent class constructor.
        """
        if "name" not in kwargs:
            raise ValueError("name is required")
        super().__init__(*args, **kwargs)

    def on_click(self, _: events.Click) -> None:
        """
        Handle the click event by logging the click and posting an ClickEvent.

        Args:
            _: The click event.
        """
        if not self.name:
            self.notify("Unknown action", severity="error")
            return

        self.post_message(self.ClickEvent(self.name))


class AboutScreen(ModalScreen):
    DEFAULT_CSS = """

    AboutScreen {
        align: center middle;
        content-align: center top;
    }

    #about_label {
        width: auto;
        height: 2;
    }

    #about_container {
        padding: 0 1;
        margin: 0 0;
        width: 50;
        height: 12;
        border: thick $background 80%;
        background: $surface;
        layout: vertical;
    }

    #window-header {
        width: 100%;
        height: 1;
        content-align: center top;
        text-style: bold;
        padding: 0 0;
        margin: 0 0;
    }

    #window-content {
        padding: 0 5 ;
        margin: 0 0;
        align: center middle;
        content-align: center top;
        height: 7;
    }

     #logo {
        padding: 0 0;
        margin: 0 0;
        width: 15;
        height: 10;
        align: center middle;
        content-align: center top;
    }

    #about_controls {
        padding: 0 0;
        height: 3;
    }
    """
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def __init__(self, terraform_version, platform, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not terraform_version:
            raise ValueError("terraform_version is required")
        if not platform:
            raise ValueError("platform is required")
        self.terraform_version = terraform_version
        self.platform = platform

    def compose(self) -> ComposeResult:
        yield Container(
            Label("🦄 About TerraLand", id="window-header"),
            Horizontal(
                Vertical(
                    Label(f"TerraLand {__version__}", id="title"),
                    Static(
                        f"Terraform version: {self.terraform_version}",
                        classes="about_label",
                    ),
                    Static(
                        f"Platform: {self.platform}",
                        classes="about_label",
                    ),
                    Static("Powered by: the-impact-craft", classes="about_label"),
                    id="window-content",
                )
            ),
            Horizontal(
                ModalControlLabel("Close", name="close", id="close", classes="button"),
                ModalControlLabel("Copy", name="copy", id="copy", classes="button"),
                id="about_controls",
            ),
            id="about_container",
        )

    def on_modal_control_label_click_event(self, message: ModalControlLabel.ClickEvent) -> None:
        """
        Handle the click event by logging the click and posting an ModalControlLabel.ClickEvent.
        :param message:
        :return:
        """

        if message.action == "close":
            self.app.pop_screen()
        elif message.action == "copy":
            try:
                self.app.copy_to_clipboard(
                    f"""
                TerraLand {__version__}
                Terraform version: {self.terraform_version}
                Platform: {self.platform}
                Powered by: the-impact-craft
                """
                )
            except Exception as e:
                self.notify(str(e), severity="error")
            else:
                self.notify("Copied to clipboard", severity="information")
