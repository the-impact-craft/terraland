import sys

from terraland.presentation.cli.action_handlers.base import BaseTerraformActionHandler
from terraland.presentation.cli.action_handlers.main import action_handler
from terraland.presentation.cli.screens.about.main import AboutScreen


@action_handler("about")
class AboutHandler(BaseTerraformActionHandler):
    def handle(self, *args, **kwargs):
        terraform_version = (
            self.app.terraform_version.terraform_version if self.app.terraform_version else "(undefined)"
        )
        platform = self.app.terraform_version.platform if self.app.terraform_version else sys.platform

        if self.app.terraform_version and self.app.terraform_version.terraform_outdated:
            terraform_version = f"{terraform_version} (outdated)"

        self.app.push_screen(
            AboutScreen(
                terraform_version=terraform_version,
                platform=platform,
            )
        )
