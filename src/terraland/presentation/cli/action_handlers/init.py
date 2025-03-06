from terraland.domain.terraform.core.entities import InitSettings
from terraland.infrastructure.terraform.core.command_builders.terraform_init_command_builder import \
    TerraformInitCommandBuilder
from terraland.presentation.cli.action_handlers.base import BaseTerraformActionHandler
from terraland.presentation.cli.action_handlers.main import action_handler
from terraland.presentation.cli.entities.terraform_command_executor import TerraformCommandExecutor
from terraland.presentation.cli.screens.tf_command_output.main import TerraformCommandOutputScreen
from terraland.presentation.cli.screens.tf_init.main import InitSettingsScreen


@action_handler("init")
class InitHandler(BaseTerraformActionHandler):
    def handle(self, *args, **kwargs):
        """
        Displays the initialization settings screen and sets up the callback
        to handle the initialization apply request.

        This method pushes the InitSettingsScreen onto the application's screen
        stack and assigns the init_handler method as the callback to process
        the settings once they are applied.
        """
        self.app.push_screen(InitSettingsScreen(), callback=self.init_handler)
        
    def init_handler(self, settings: InitSettings):
        """
        Handles the initialization of apply request for the settings screen.

        This asynchronous method executes a sequence of steps to handle the initialization
        apply request by interacting with the content view, adding a specific tab, and
        initiating the application plan. It performs necessary operations upon receipt of
        an initialization apply request event.

        Args:
            settings (InitSettings): The initialization apply request
                event that triggers this handler.
        """
        if not settings:
            return

        output_screen = TerraformCommandOutputScreen()
        self.app.push_screen(output_screen)

        command = TerraformInitCommandBuilder().build_from_settings(settings)

        if self.app.tf_command_executor:
            self.app.tf_command_executor.cancel()

        self.app.tf_command_executor = TerraformCommandExecutor(command=command)

        worker = self.app.run_worker(
            self.app.run_tf_action(
                command,
                error_message="Failed to apply plan settings.",
                output_screen=output_screen
            ),
            exit_on_error=True,
            thread=True,
            group="tf_command_worker"
        )
        
        self.app.tf_command_executor.worker = worker
