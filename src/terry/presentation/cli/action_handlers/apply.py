from terry.presentation.cli.action_handlers.base import BaseTerraformActionHandler
from terry.presentation.cli.action_handlers.main import action_handler
from terry.presentation.cli.screens.tf_apply.main import ApplySettingsScreen


@action_handler("apply")
class ApplyHandler(BaseTerraformActionHandler):
    def handle(self, *args, **kwargs):
        self.app.push_screen(ApplySettingsScreen())
