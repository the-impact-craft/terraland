from terry.presentation.cli.action_handlers.base import BaseTerraformActionHandler
from terry.presentation.cli.action_handlers.main import action_handler
from terry.presentation.cli.screens.tf_format.main import FormatSettingsScreen


@action_handler("fmt")
class FormatHandler(BaseTerraformActionHandler):
    def handle(self, *args, **kwargs):
        self.app.push_screen(FormatSettingsScreen())
