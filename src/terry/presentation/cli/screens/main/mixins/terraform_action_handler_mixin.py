import asyncio


from terry.domain.terraform.core.entities import TerraformFormatScope, CommandStatus
from terry.infrastructure.shared.command_process_context_manager import CommandProcessContextManager
from terry.infrastructure.shared.command_utils import process_stdout_stderr
from terry.infrastructure.terraform.core.commands_builders import (
    TerraformPlanCommandBuilder,
    TerraformInitCommandBuilder,
    TerraformApplyCommandBuilder,
)
from terry.infrastructure.terraform.core.exceptions import TerraformFormatException, TerraformValidateException
from terry.presentation.cli.action_handlers.main import action_handler_registry
from terry.presentation.cli.custom.messages.tf_apply_action_request import ApplyActionRequest
from terry.presentation.cli.custom.messages.tf_format_action_request import FormatActionRequest
from terry.presentation.cli.custom.messages.tf_init_action_request import InitActionRequest
from terry.presentation.cli.custom.messages.tf_plan_action_request import PlanActionRequest
from terry.presentation.cli.custom.messages.tf_validate_action_request import ValidateActionRequest
from terry.presentation.cli.custom.widgets.clickable_tf_action_label import ClickableTfActionLabel
from terry.presentation.cli.entities.terraform_command_executor import TerraformCommandExecutor
from terry.presentation.cli.screens.main.containers.content import Content
from terry.presentation.cli.screens.tf_command_output.main import TerraformCommandOutputScreen


class TerraformActionHandlerMixin:
    def on_clickable_tf_action_label_click_event(self, event: ClickableTfActionLabel.ClickEvent) -> None:
        """
        Handle the clickable label click event in the Terry application.

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

    def on_format_action_request(self, event: FormatActionRequest) -> None:
        """
        Handle the format apply request event in the Terry application.

        This method processes the format apply request event triggered by the user in the format settings screen.

        Args:
            event (FormatActionRequest): The event containing the format settings to apply.

        Raises:
            Exception: If the format settings cannot be applied.
        """
        format_scope = None
        if event.format.value == TerraformFormatScope.CURRENT_FILE.value:
            content_tabs = self.query_one(Content)
            format_scope = content_tabs.active_tab
            if not format_scope:
                self.notify("No file selected.", severity="warning")
                return

        try:
            output = self.terraform_core_service.fmt(format_scope)
        except TerraformFormatException as e:
            self.log.error(str(e))
            self.notify("Failed to apply format settings.", severity="error")
            self.write_command_log(e.command, CommandStatus.ERROR, e.message)
            return
        else:
            self.notify("Format settings applied successfully.", severity="information")
            self.log.info(output.output)
            self.write_command_log(output.command, CommandStatus.SUCCESS, output.output)

    def on_validate_action_request(self, event: ValidateActionRequest) -> None:
        """
        Handles the `ValidateActionRequest` event to validate and apply Terraform
        formatting for the specified scope. The handler determines the scope of
        formatting (e.g., the currently active file), processes the formatting via the
        Terraform core service, and provides user notifications for both success and
        failure cases. Command logs are updated accordingly.

        Args:
            event: An instance of `ValidateActionRequest` containing the format request
                details, such as the scope of formatting to be applied.
        """
        try:
            output = self.terraform_core_service.validate(event.settings)
        except TerraformValidateException as e:
            self.log.error(str(e))
            self.notify("Project validation failed.", severity="error")
            self.write_command_log(e.command, CommandStatus.ERROR, e.message)
            return
        else:
            self.notify("Project has been validate.", severity="information")
            self.log.info(output.output)
            self.write_command_log(output.command, CommandStatus.SUCCESS, output.output)

    async def on_plan_action_request(self, event: PlanActionRequest):
        """
        Handles the application of a plan request. It retrieves the content component, dynamically creates a tab for
        the plan, and initiates the execution of the plan using the corresponding event and tab.

        Arguments:
            event (PlanApplyRequest): The event containing the plan settings to apply.
        """
        self.push_screen(TerraformCommandOutputScreen())
        command = TerraformPlanCommandBuilder().build_from_settings(event.settings)
        if self._tf_command_executor:
            self._tf_command_executor.cancel()

        worker = self.run_worker(
            self.run_tf_action(command, "Failed to apply plan settings."),
            exit_on_error=True,
            thread=True,
            group="tf_command_worker",
        )
        self._tf_command_executor = TerraformCommandExecutor(command=command, worker=worker)

    async def on_init_action_request(self, event: InitActionRequest):
        """
        Handles the initialization of apply request for the settings screen.

        This asynchronous method executes a sequence of steps to handle the initialization
        apply request by interacting with the content view, adding a specific tab, and
        initiating the application plan. It performs necessary operations upon receipt of
        an initialization apply request event.

        Args:
            event (InitActionRequest): The initialization apply request
                event that triggers this handler.
        """
        self.push_screen(TerraformCommandOutputScreen())
        command = TerraformInitCommandBuilder().build_from_settings(event.settings)

        if self._tf_command_executor:
            self._tf_command_executor.cancel()

        worker = self.run_worker(
            self.run_tf_action(command, error_message="Failed to apply plan settings."),
            exit_on_error=True,
            thread=True,
            group="tf_command_worker",
        )
        self._tf_command_executor = TerraformCommandExecutor(command=command, worker=worker)

    async def on_apply_action_request(self, event: ApplyActionRequest):
        """
        Handles the ApplyActionRequest event by executing a Terraform apply command.

        This method is invoked to handle requests for applying Terraform plans defined
        in the settings provided by the event. It initializes the Terraform environment,
        executes the apply command, and ensures the proper handling of command execution
        through a dedicated thread and worker.

        Args:
            event: The ApplyActionRequest event containing settings required for
                applying the Terraform plan.

        """
        # Todo: check if we can reuse logic for init, plan, apply
        self.push_screen(TerraformCommandOutputScreen())
        command = TerraformApplyCommandBuilder().build_from_settings(event.settings)

        if self._tf_command_executor:
            self._tf_command_executor.cancel()

        worker = self.run_worker(
            self.run_tf_action(command, error_message="Failed to apply settings."),
            exit_on_error=True,
            thread=True,
            group="tf_command_worker",
        )
        self._tf_command_executor = TerraformCommandExecutor(command=command, worker=worker)

    def on_terraform_command_output_screen_close(self, _: TerraformCommandOutputScreen.Close):
        if self._tf_command_executor:
            self._tf_command_executor.cancel()

    async def run_tf_action(self, tf_command: list[str], error_message: str):
        """
        Executes an asynchronous plan based on the specified tab name and updates the UI
        elements to reflect the ongoing process. The method logs the corresponding command
        and its output in real time, providing detailed feedback to the user. In case of an
        error, appropriate notifications are shown, and the error is logged.

        Arguments:
           tf_command (list[str]): The Terraform command to execute.
            error_message (str): The error message to display in case of an error.
        """

        await asyncio.sleep(2)
        tf_command_str = " ".join(tf_command)
        area = self.app.query_one(TerraformCommandOutputScreen)
        manager = CommandProcessContextManager(tf_command, str(self.work_dir))
        self._tf_command_executor.command_process = manager  # type: ignore
        with manager as (stdin, stdout, stderr):
            area.stdin = stdin
            for line in process_stdout_stderr(stdout, stderr):
                area.write_log(line)
        area.stdin = None

        if manager.error:
            self.log.error(str(manager.error))
            self.notify(error_message, severity="error")
            self.write_command_log(tf_command_str, CommandStatus.ERROR, str(manager.error))
            return
