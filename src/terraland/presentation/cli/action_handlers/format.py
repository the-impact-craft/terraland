from terraland.presentation.cli.action_handlers.base import BaseTerraformActionHandler
from terraland.presentation.cli.action_handlers.main import action_handler
from terraland.presentation.cli.screens.tf_format.main import FormatSettingsScreen


@action_handler("fmt")
class FormatHandler(BaseTerraformActionHandler):
    def handle(self, *args, **kwargs):
        self.app.push_screen(FormatSettingsScreen())
