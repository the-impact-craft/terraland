from pathlib import Path

from terraland.domain.terraform.core.entities import FormatSettings


class TerraformFormatCommandBuilder:
    def __init__(self):
        """Initialize the base terraform apply command."""
        self.command = ["terraform", "fmt"]

    def add_path(self, path: str | Path) -> "TerraformFormatCommandBuilder":
        self.command.extend([str(path)])
        return self

    def build(self) -> list[str]:
        """Build and return the final terraform apply command."""
        return self.command

    def build_from_settings(self, settings: FormatSettings) -> list[str]:
        if settings.path:
            self.add_path(settings.path)
        return self.build()
