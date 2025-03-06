from terraland.domain.operation_system.entities import EnvVariableFilter
from terraland.domain.terraform.core.entities import PlanSettings
from terraland.infrastructure.terraform.core.command_builders.terraform_plan_command_builder import \
    TerraformPlanCommandBuilder
from terraland.presentation.cli.action_handlers.base import BaseTerraformActionHandler
from terraland.presentation.cli.action_handlers.main import action_handler
from terraland.presentation.cli.entities.terraform_command_executor import TerraformCommandExecutor
from terraland.presentation.cli.screens.tf_command_output.main import TerraformCommandOutputScreen
from terraland.presentation.cli.screens.tf_plan.main import PlanSettingsScreen
from terraland.settings import ENV_VARS_PREFIXES


@action_handler("plan")
class PlanHandler(BaseTerraformActionHandler):
    def handle(self, *args, **kwargs):
        """
        Handles the "plan" action by retrieving environment variables and displaying
        the PlanSettingsScreen. It filters environment variables based on predefined
        prefixes and handles any exceptions that occur during retrieval by notifying
        the user of the failure.
        """
        operation_system_service = self.app.operation_system_service
        try:
            env_vars_filter = EnvVariableFilter(prefix=ENV_VARS_PREFIXES)
            env_vars = operation_system_service.list_environment_variables(env_vars_filter)
        except Exception:
            self.app.notify("Failed to retrieve environment variables", severity="error")
            return
        self.app.push_screen(PlanSettingsScreen(env_vars), callback=self.plan_handler)

    def plan_handler(self, settings: PlanSettings):
        """
        Handles the `PlanActionRequest` event to plan and apply Terraform changes for the specified scope.
        The handler determines the scope of changes (e.g., the currently active file), processes the plan
        via the Terraform core service, and provides user notifications for both success and failure cases.
        Command logs are updated accordingly.

        Args:
            settings: An instance of `PlanSettings` containing the plan request details, such as the scope of changes to be applied.
        """
        if not settings:
            return

        output_screen = TerraformCommandOutputScreen()
        self.app.push_screen(output_screen)
        command = TerraformPlanCommandBuilder().build_from_settings(settings)

        env_vars = {var.name: var.value for var in settings.env_vars} if settings.env_vars else None

        if self.app.tf_command_executor:
            self.app.tf_command_executor.cancel()

        self.app.tf_command_executor = TerraformCommandExecutor(command=command)

        worker = self.app.run_worker(
            self.app.run_tf_action(
                command, "Failed to apply plan settings.", env_vars=env_vars, output_screen=output_screen
            ),
            exit_on_error=True,
            thread=True,
            group="tf_command_worker",
        )
        
        self.app.tf_command_executor.worker = worker
