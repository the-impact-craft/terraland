from terraland.presentation.cli.action_handlers.base import BaseTerraformActionHandler
from terraland.presentation.cli.action_handlers.main import action_handler
from terraland.presentation.cli.screens.tf_init.main import InitSettingsScreen


@action_handler("init")
class InitHandler(BaseTerraformActionHandler):
    def handle(self, *args, **kwargs):
        self.app.push_screen(InitSettingsScreen())
