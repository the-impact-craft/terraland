from dataclasses import dataclass

from textual.worker import Worker


@dataclass
class TerraformCommandExecutor:
    command: list[str]
    worker: Worker | None = None
    command_process = None

    def cancel(self):
        if self.command_process:
            self.command_process.terminate_process()
            self.command_process = None
        if self.worker:
            self.worker.cancel()
            self.worker = None
        self.command = []
