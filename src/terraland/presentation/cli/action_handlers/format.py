from terraland.domain.terraform.core.entities import FormatScope, TerraformFormatScope, FormatSettings
from terraland.infrastructure.terraform.core.command_builders.terraform_format_command_builder import \
    TerraformFormatCommandBuilder
from terraland.presentation.cli.action_handlers.base import BaseTerraformActionHandler
from terraland.presentation.cli.action_handlers.main import action_handler
from terraland.presentation.cli.entities.terraform_command_executor import TerraformCommandExecutor
from terraland.presentation.cli.screens.main.containers.content import Content
from terraland.presentation.cli.screens.tf_format.main import FormatSettingsScreen


@action_handler("fmt")
class FormatHandler(BaseTerraformActionHandler):
    def handle(self, *args, **kwargs):
        """
        Initiates the format settings screen in the TerraLand application.

        This method pushes the FormatSettingsScreen onto the application's screen stack,
        allowing the user to configure and apply formatting settings. The format_handler
        method is set as a callback to handle the user's selection.
        """
        self.app.push_screen(FormatSettingsScreen(), callback=self.format_handler)
        
    def format_handler(self, format_setting: FormatScope | None):
        """
        Handle the format apply request event in the TerraLand application.

        This method processes the format apply request event triggered by the user in the format settings screen.

        Args:
            format_setting (FormatScope): The event containing the format settings to apply.

        Raises:
            Exception: If the format settings cannot be applied.
        """
        if not format_setting:
            return

        format_scope = None
        if format_setting.value == TerraformFormatScope.CURRENT_FILE.value:
            content_tabs = self.app.query_one(Content)
            format_scope = content_tabs.active_tab
            if not format_scope:
                self.app.notify("No file selected.", severity="warning")
                return

        settings = FormatSettings(path=format_scope)
        command = TerraformFormatCommandBuilder().build_from_settings(settings)

        if self.app.tf_command_executor:
            self.app.tf_command_executor.cancel()

        self.app.tf_command_executor = TerraformCommandExecutor(command=command)

        worker = self.app.run_worker(
            self.app.run_tf_action(command, "Failed to format."),
            exit_on_error=True,
            thread=True,
            group="tf_command_worker",
        )
        
        self.app.tf_command_executor.worker = worker
