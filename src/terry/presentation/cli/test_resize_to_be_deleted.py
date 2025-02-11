from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static, Rule
from textual.events import MouseMove, MouseDown, MouseUp


class ResizableContainer(Horizontal):
    """Custom container with a draggable separator."""

    def __init__(self):
        super().__init__()
        self.left_panel = Static("Left Panel", classes="panel")
        self.right_panel = Static("Right Panel", classes="panel")
        self.separator = Rule(orientation="vertical", classes="separator")  # Draggable separator

        self.dragging = False
        self.last_x = 0

    def compose(self) -> ComposeResult:
        yield self.left_panel
        yield self.separator
        yield self.right_panel

    def on_mouse_down(self, event: MouseDown) -> None:
        """Start dragging when the separator is clicked."""
        self.log(event)
        self.dragging = True
        self.last_x = event.x

    def on_mouse_move(self, event: MouseMove) -> None:
        """Resize panels when dragging."""
        if self.dragging:
            dx = event.x - self.last_x
            self.last_x = event.x

            # Adjust panel widths dynamically
            left_width = max(10, self.left_panel.styles.width.value + dx)  # type: ignore
            right_width = max(10, self.right_panel.styles.width.value - dx)  # type: ignore

            self.left_panel.styles.width = left_width
            self.right_panel.styles.width = right_width
            self.refresh()

    def on_mouse_up(self, event: MouseUp) -> None:
        """Stop drqagging when mouse is released."""
        self.dragging = False


class ResizableApp(App):
    """Main app with a resizable layout."""

    def compose(self) -> ComposeResult:
        yield ResizableContainer()

    CSS = """
    Screen {
        layout: horizontal;
    }

    .panel {
        background: blue;
        color: white;
        padding: 2;
        width: 1fr;
    }

    """


if __name__ == "__main__":
    ResizableApp().run()
