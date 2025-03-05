from terraland.domain.operation_system.entities import EnvVariableFilter
from terraland.presentation.cli.action_handlers.base import BaseTerraformActionHandler
from terraland.presentation.cli.action_handlers.main import action_handler
from terraland.presentation.cli.screens.tf_apply.main import ApplySettingsScreen
from terraland.settings import ENV_VARS_PREFIXES


@action_handler("apply")
class ApplyHandler(BaseTerraformActionHandler):
    def handle(self, *args, **kwargs):
        operation_system_service = self.app.operation_system_service
        try:
            env_vars_filter = EnvVariableFilter(prefix=ENV_VARS_PREFIXES)
            env_vars = operation_system_service.list_environment_variables(env_vars_filter)
        except Exception:
            self.app.notify("Failed to retrieve environment variables", severity="error")
            return
        self.app.push_screen(ApplySettingsScreen(env_vars))
