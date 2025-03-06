from pathlib import Path
from typing import Union, List, Dict

from terraland.domain.terraform.core.entities import InitSettings


class TerraformInitCommandBuilder:
    """Builder class for Terraform init commands."""

    def __init__(self):
        """Initialize the base terraform init command."""
        self.command = ["terraform", "init"]

    def add_disable_backend(self) -> "TerraformInitCommandBuilder":
        """Add the `-backend=false` flag."""
        self.command.append("-backend=false")
        return self

    def add_backend_config(self, backend_config: Dict[str, str]) -> "TerraformInitCommandBuilder":
        """Add backend configuration key-value pairs."""
        for key, value in backend_config.items():
            self.command.extend(["-backend-config", f"{key}={value}"])
        return self

    def add_backend_config_path(
        self, backend_config_path: Union[str, Path, List[str | Path]]
    ) -> "TerraformInitCommandBuilder":
        """Add backend configuration file(s)."""
        if isinstance(backend_config_path, list):
            for path in backend_config_path:
                self.command.extend(["-backend-config", f"{path}"])
        else:
            self.command.extend(["-backend-config", f"{backend_config_path}"])
        return self

    def add_force_copy(self) -> "TerraformInitCommandBuilder":
        """Add the `-force-copy` flag."""
        self.command.append("-force-copy")
        return self

    def add_disable_download(self) -> "TerraformInitCommandBuilder":
        """Add the `-get=false` flag."""
        self.command.append("-get=false")
        return self

    def add_disable_input(self) -> "TerraformInitCommandBuilder":
        """Add the `-input=false` flag."""
        self.command.append("-input=false")
        return self

    def add_disable_hold_lock(self) -> "TerraformInitCommandBuilder":
        """Add the `-lock=false` flag."""
        self.command.append("-lock=false")
        return self

    def add_plugin_dir(self, plugin_dir: Union[str, Path, List[str | Path]]) -> "TerraformInitCommandBuilder":
        """Add plugin directory or directories."""
        if isinstance(plugin_dir, list):
            for dir in plugin_dir:
                self.command.extend(["-plugin-dir", f"{dir}"])
        else:
            self.command.extend(["-plugin-dir", f"{plugin_dir}"])
        return self

    def add_reconfigure(self) -> "TerraformInitCommandBuilder":
        """Add the `-reconfigure` flag."""
        self.command.append("-reconfigure")
        return self

    def add_migrate_state(self) -> "TerraformInitCommandBuilder":
        """Add the `-migrate-state` flag."""
        self.command.append("-migrate-state")
        return self

    def add_upgrade(self) -> "TerraformInitCommandBuilder":
        """Add the `-upgrade` flag."""
        self.command.append("-upgrade")
        return self

    def add_ignore_remote_version(self) -> "TerraformInitCommandBuilder":
        """Add the `-ignore-remote-version` flag."""
        self.command.append("-ignore-remote-version")
        return self

    def add_test_directory(self, test_directory: Union[str, Path, list[str | Path]]) -> "TerraformInitCommandBuilder":
        """Add test directory or directories."""
        if isinstance(test_directory, list):
            for directory in test_directory:
                self.command.extend(["-test-directory", f"{directory}"])
        else:
            self.command.extend(["-test-directory", f"{test_directory}"])
        return self

    def build(self) -> list[str]:
        """Build and return the final terraform init command."""
        return self.command

    def build_from_settings(self, settings: InitSettings) -> list[str]:
        if settings.disable_backend:
            self.add_disable_backend()
        if settings.backend_config:
            self.add_backend_config(settings.backend_config)
        if settings.backend_config_path:
            self.add_backend_config_path(settings.backend_config_path)
        if settings.force_copy:
            self.add_force_copy()
        if settings.disable_download:
            self.add_disable_download()
        if settings.disable_input:
            self.add_disable_input()
        if settings.disable_hold_lock:
            self.add_disable_hold_lock()
        if settings.plugin_dir:
            if isinstance(settings.plugin_dir, list):
                for dir in settings.plugin_dir:
                    self.add_plugin_dir(dir)
            else:
                self.add_plugin_dir(settings.plugin_dir)
        if settings.reconfigure:
            self.add_reconfigure()
        if settings.migrate_state:
            self.add_migrate_state()
        if settings.upgrade:
            self.add_upgrade()
        if settings.ignore_remote_version:
            self.add_ignore_remote_version()
        if settings.test_directory:
            if isinstance(settings.test_directory, list):
                for directory in settings.test_directory:
                    self.add_test_directory(directory)
            else:
                self.add_test_directory(settings.test_directory)
        return self.build()