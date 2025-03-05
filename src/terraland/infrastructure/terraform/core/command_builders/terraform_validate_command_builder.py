from pathlib import Path
from typing import Union

from terraland.domain.terraform.core.entities import ValidateSettings


class TerraformValidateCommandBuilder:
    """Builder class for Terraform validate commands."""

    def __init__(self):
        """Initialize the base terraform validate command."""
        self.command = ["terraform", "validate"]

    def add_no_tests(self) -> "TerraformValidateCommandBuilder":
        """Add the `-no-tests` flag."""
        self.command.append("-no-tests")
        return self

    def add_test_directory(
        self, test_directory: Union[str, Path, list[str | Path]]
    ) -> "TerraformValidateCommandBuilder":
        """Add test directory or directories."""
        if isinstance(test_directory, list):
            for directory in test_directory:
                self.command.extend(["-test-directory", f"{directory}"])
        else:
            self.command.extend(["-test-directory", f"{test_directory}"])
        return self

    def build(self) -> list[str]:
        """Build and return the final terraform validate command."""
        return self.command

    def build_from_settings(self, settings: ValidateSettings) -> list[str]:
        if settings.no_tests:
            self.add_no_tests()
        if settings.test_directory: 
            if isinstance(settings.test_directory, list):
                for directory in settings.test_directory:
                    self.add_test_directory(directory)
            else:
                self.add_test_directory(settings.test_directory)
        return self.build()
