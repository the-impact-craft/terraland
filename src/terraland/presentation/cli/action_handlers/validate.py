from terraland.domain.terraform.core.entities import ValidateSettings
from terraland.infrastructure.terraform.core.exceptions import TerraformValidateException
from terraland.presentation.cli.action_handlers.base import BaseTerraformActionHandler
from terraland.presentation.cli.action_handlers.main import action_handler
from terraland.presentation.cli.screens.tf_validate.main import ValidateSettingsScreen


@action_handler("validate")
class ValidateHandler(BaseTerraformActionHandler):
    def handle(self, *args, **kwargs):
        """
        Initiates the validation process by displaying the ValidateSettingsScreen
        and setting up the callback to handle the validation logic.
        """
        self.app.push_screen(ValidateSettingsScreen(), callback=self.validate_handler)
        
    def validate_handler(self, settings: ValidateSettings | None):
        """
        Handles the `ValidateActionRequest` event to validate and apply Terraform
        formatting for the specified scope. The handler determines the scope of
        formatting (e.g., the currently active file), processes the formatting via the
        Terraform core service, and provides user notifications for both success and
        failure cases. Command logs are updated accordingly.

        Args:
            settings: An instance of `ValidateSettings` containing the format request
                details, such as the scope of formatting to be applied.
        """
        if not settings:
            return

        try:
            output = self.app.terraform_core_service.validate(settings)
            self.app.log_success("Project has been validated.", output.command, output.output)
        except TerraformValidateException as ex:
            self.app.log_error("Project validation failed.", ex.command, ex.message)
