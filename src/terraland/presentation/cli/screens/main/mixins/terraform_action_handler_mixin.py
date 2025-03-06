from contextlib import contextmanager
from datetime import datetime

from dependency_injector.wiring import Provide
from textual.screen import Screen

from terraland.infrastructure.shared.command_process_context_manager import CommandProcessContextManager
from terraland.infrastructure.shared.command_utils import process_stdout_stderr
from terraland.presentation.cli.action_handlers.main import action_handler_registry
from terraland.presentation.cli.cache import TerraLandCache
from terraland.presentation.cli.di_container import DiContainer
from terraland.presentation.cli.entities.command_cache import CommandCache
from terraland.presentation.cli.entities.terraform_command_executor import TerraformCommandExecutor

from terraland.presentation.cli.messages.tf_rerun_command import RerunCommandRequest
from terraland.presentation.cli.screens.tf_command_output.main import TerraformCommandOutputScreen
from terraland.presentation.cli.widgets.clickable_tf_action_label import ClickableTfActionLabel


class TerraformActionHandlerMixin:
    required_methods = [
        "query_one",
        "notify",
        "log",
        "write_command_log",
        "push_screen",
    ]

    required_attributes = [
        "work_dir",
        "terraform_core_service",
    ]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        for attribute in cls.required_attributes:
            if not hasattr(cls, attribute):
                raise AttributeError(f"Class {cls.__name__} must have attribute {attribute}")

        for method in cls.required_methods:
            if not hasattr(cls, method) or not callable(getattr(cls, method)):
                raise TypeError(f"Class {cls.__name__} must implement method {method}")

    def on_clickable_tf_action_label_click_event(self, event: ClickableTfActionLabel.ClickEvent) -> None:
        """
        Handle the clickable label click event in the TerraLand application.

        This method processes the clickable label click events triggered by the user in the main screen.

        Args:
            event (ClickableTfActionLabel.Click): The event containing the action to handle.

        Raises:
            Exception: If the action handler fails.
        """
        handler = action_handler_registry.get(event.action)
        if not handler:
            return
        handler(self).handle()


    async def on_rerun_command_request(self, event: RerunCommandRequest):
        output_screen = None
        if event.run_in_modal:
            output_screen = TerraformCommandOutputScreen()
            self.push_screen(output_screen)  # type: ignore
        if self.tf_command_executor:
            self.tf_command_executor.cancel()
        worker = self.run_worker(  # type: ignore
            self.run_tf_action(event.command, error_message=event.error_message, output_screen=output_screen),
            exit_on_error=True,
            thread=True,
            group="tf_command_worker",
        )
        self.tf_command_executor = TerraformCommandExecutor(command=event.command, worker=worker)

    def on_terraform_command_output_screen_close(self, _: TerraformCommandOutputScreen.Close):
        if self.tf_command_executor:
            self.tf_command_executor.cancel()

    async def run_tf_action(
        self,
        tf_command: list[str],
        error_message: str,
        env_vars: dict | None = None,
        cache: TerraLandCache = Provide[DiContainer.cache],
        output_screen: Screen | None = None,
    ):
        """
        Executes an asynchronous plan based on the specified tab name and updates the UI
        elements to reflect the ongoing process. The method logs the corresponding command
        and its output in real time, providing detailed feedback to the user. In case of an
        error, appropriate notifications are shown, and the error is logged.

        Arguments:
            tf_command (list[str]): The Terraform command to execute.
            error_message (str): The error message to display in case of an error.
            env_vars(dict | None): The environment variables to set during command execution
            cache (TerraLandCache): The cache instance to store the executed commands
            output_screen (Screen): The screen to display the command output.
        """

        tf_command_str = " ".join(tf_command)

        manager = CommandProcessContextManager(
            tf_command,
            self.operation_system_service,  # type: ignore
            str(self.work_dir),  # type: ignore
            env_vars,
        )
        self.tf_command_executor.command_process = manager  # type: ignore

        cache.extend(
            "commands",
            CommandCache(
                tf_command, datetime.now(), run_in_modal=output_screen is not None, error_message=error_message
            ),
        )  # type: ignore

        if self.history_sidebar:  # type: ignore
            self.history_sidebar.refresh_content()  # type: ignore

        with self.paused_system_monitoring():
            with manager as (stdin, stdout, stderr):
                self._handle_logs(tf_command_str, output_screen, stdin, stdout, stderr)

        if manager.error:
            self.log_error(error_message, tf_command_str, str(manager.error)) # type: ignore
            return



    def _get_ui_area(self):
        """Sets up the UI output area based on the background execution flag."""
        return self.app.query_one(TerraformCommandOutputScreen)  # type: ignore

    def _handle_logs(self, command, output_screen, stdin, stdout, stderr):
        """Handles logging the process output and updating the UI."""
        output = []

        if output_screen:
            with output_screen.stdin_context(stdin):
                for line in process_stdout_stderr(stdout, stderr):
                    output_screen.write_log(line)
                    output.append(line)
        else:
            for line in process_stdout_stderr(stdout, stderr):
                output.append(line)

        self.log_success("Command executed.", command, "\n".join(output)) # type: ignore

    @contextmanager
    def paused_system_monitoring(self):
        try:
            self.pause_system_monitoring = True
            yield
        finally:
            self.pause_system_monitoring = False
