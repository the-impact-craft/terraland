from terry.presentation.cli.action_handlers.base import BaseTerraformActionHandler
from terry.presentation.cli.action_handlers.main import action_handler
from terry.presentation.cli.screens.tf_validate.main import ValidateSettingsScreen


@action_handler("validate")
class ValidateHandler(BaseTerraformActionHandler):
    def handle(self, *args, **kwargs):
        self.app.push_screen(ValidateSettingsScreen())
