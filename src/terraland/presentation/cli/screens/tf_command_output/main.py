from contextlib import contextmanager
from dataclasses import dataclass
from typing import IO

from textual import on
from textual.containers import Container
from textual.message import Message
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Input, RichLog


class TerraformCommandOutputScreen(ModalScreen):
    CONTAINER_ID = "terraform-command-output"
    BINDINGS = [("escape", "exit", "Pop screen")]
    CSS_PATH = "styles.tcss"
    stdin: reactive[IO[bytes] | None] = reactive(None)

    @dataclass
    class Close(Message):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._log = None
        self._input_area: Input | None = None
        self._text_area: RichLog | None = None
        self.log_content_array = []

    def compose(self):
        self._input_area = Input(id="input-area")
        self._text_area = RichLog(highlight=True, markup=False)

        with Container(id=self.CONTAINER_ID):
            yield self._text_area
            yield self._input_area

    def write_log(self, log: str):
        if not self._text_area:
            return
        self._text_area.write(log)

        if "Enter a value:" in log and self._input_area:
            self._input_area.focus()

    def watch_stdin(self):
        if self._input_area:
            self._input_area.disabled = self.stdin is None

    @on(Input.Submitted)
    def _on_input(self, message):
        if self._text_area is None:
            return
        self._text_area.write(message.value)

        if self.stdin is None:
            self.log("STDIN is not available.")
            return

        self.stdin.write(f"{message.value}\n")  # type: ignore
        self.stdin.flush()
        if self._input_area:
            self._input_area.clear()
            self._input_area.blur()
        self._text_area.focus()

    def action_exit(self):
        self.post_message(self.Close())
        self.app.pop_screen()

    @contextmanager
    def stdin_context(self, stdin: IO[bytes]):
        self.stdin = stdin
        try:
            yield
        finally:
            self.stdin = None
            self.log("STDIN is closed.")
