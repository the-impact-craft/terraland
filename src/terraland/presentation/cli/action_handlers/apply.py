from terraland.domain.operation_system.entities import EnvVariableFilter
from terraland.domain.terraform.core.entities import ApplySettings
from terraland.infrastructure.terraform.core.command_builders.terraform_apply_command_builder import \
    TerraformApplyCommandBuilder
from terraland.presentation.cli.action_handlers.base import BaseTerraformActionHandler
from terraland.presentation.cli.action_handlers.main import action_handler
from terraland.presentation.cli.entities.terraform_command_executor import TerraformCommandExecutor
from terraland.presentation.cli.screens.tf_apply.main import ApplySettingsScreen
from terraland.presentation.cli.screens.tf_command_output.main import TerraformCommandOutputScreen
from terraland.settings import ENV_VARS_PREFIXES


@action_handler("apply")
class ApplyHandler(BaseTerraformActionHandler):
    def handle(self, *args, **kwargs):
        """
        Handles the retrieval of environment variables and displays the ApplySettingsScreen.

        This method uses the operation system service to filter and list environment variables
        based on predefined prefixes. If successful, it pushes the ApplySettingsScreen with the
        retrieved environment variables and sets the apply_handler as a callback. In case of failure,
        it notifies the user with an error message.
        """
        operation_system_service = self.app.operation_system_service
        try:
            env_vars_filter = EnvVariableFilter(prefix=ENV_VARS_PREFIXES)
            env_vars = operation_system_service.list_environment_variables(env_vars_filter)
        except Exception:
            self.app.notify("Failed to retrieve environment variables", severity="error")
            return
        self.app.push_screen(ApplySettingsScreen(env_vars), callback=self.apply_handler)
        
    def apply_handler(self, settings: ApplySettings):
        """
        Handles the `ApplyActionRequest` event to apply Terraform changes for the specified scope.
        The handler determines the scope of changes (e.g., the currently active file), processes the apply
        via the Terraform core service, and provides user notifications for both success and failure cases.
        Command logs are updated accordingly.

        Args:
            settings: An instance of `ApplySettings` containing the apply request details, such as the scope of changes to be applied.
        """
        if not settings:
            return

        output_screen = TerraformCommandOutputScreen()
        self.app.push_screen(output_screen)
        command = TerraformApplyCommandBuilder().build_from_settings(settings)

        env_vars = {var.name: var.value for var in settings.env_vars} if settings.env_vars else None

        if self.app.tf_command_executor:
            self.app.tf_command_executor.cancel()

        self.app.tf_command_executor = TerraformCommandExecutor(command=command)

        worker = self.app.run_worker(
            self.app.run_tf_action(
                command, error_message="Failed to apply settings.", env_vars=env_vars, output_screen=output_screen
            ),
            exit_on_error=True,
            thread=True,
            group="tf_command_worker",
        )
        
        self.app.tf_command_executor.worker = worker
