from pathlib import Path

from terraland.domain.terraform.core.entities import ApplySettings


class TerraformApplyCommandBuilder:
    """Builder class for Terraform apply commands."""

    def __init__(self):
        """Initialize the base terraform apply command."""
        self.command = ["terraform", "apply"]

    def add_auto_approve(self) -> "TerraformApplyCommandBuilder":
        """Add the `-auto-approve` flag."""
        self.command.append("-auto-approve")
        return self

    def add_backup(self, backup: str | Path) -> "TerraformApplyCommandBuilder":
        """Add a backup file path."""
        self.command.extend(["-backup", str(backup)])
        return self

    def add_disable_backup(self) -> "TerraformApplyCommandBuilder":
        """Add the `-backup=-` flag."""
        self.command.append("-backup=-")
        return self

    def add_destroy(self) -> "TerraformApplyCommandBuilder":
        """Add the `-destroy` flag."""
        self.command.append("-destroy")
        return self

    def add_disable_lock(self) -> "TerraformApplyCommandBuilder":
        """Add the `-lock=false` flag."""
        self.command.append("-lock=false")
        return self

    def add_input(self) -> "TerraformApplyCommandBuilder":
        """Add the `-input` flag."""
        self.command.append("-input")
        return self

    def add_state(self, state: str | Path) -> "TerraformApplyCommandBuilder":
        """Add a state file path."""
        self.command.extend(["-state", str(state)])
        return self

    def add_state_out(self, state_out: str | Path) -> "TerraformApplyCommandBuilder":
        """Add a state output file path."""
        self.command.extend(["-state-out", str(state_out)])
        return self

    def app_plan_file(self, plan_file: str | Path) -> "TerraformApplyCommandBuilder":
        """Add a plan file path."""
        self.command.extend([str(plan_file)])
        return self

    def add_inline_var(self, name: str, value: str) -> "TerraformApplyCommandBuilder":
        self.command.extend(["-var", f"{name}={value}"])
        return self

    def add_var_file(self, file: str) -> "TerraformApplyCommandBuilder":
        self.command.extend(["-var-file", file])
        return self

    def build(self) -> list[str]:
        """Build and return the final terraform apply command."""
        return self.command

    def build_from_settings(self, settings: ApplySettings) -> list[str]:
        if settings.auto_approve:
            self.add_auto_approve()
        if settings.backup:
            self.add_backup(settings.backup)
        if settings.disable_backup:
            self.add_disable_backup()
        if settings.destroy:
            self.add_destroy()
        if settings.disable_lock:
            self.add_disable_lock()
        if settings.input:
            self.add_input()
        if settings.state:
            self.add_state(settings.state)
        if settings.state_out:
            self.add_state_out(settings.state_out)
        if settings.inline_vars:
            for var in settings.inline_vars:
                if not var.name or not var.value:
                    continue
                self.add_inline_var(var.name, var.value)
        if settings.var_files:
            for var_file in settings.var_files:
                self.add_var_file(var_file)
        if settings.plan:
            self.app_plan_file(f"{settings.plan[0]}")
        return self.build()
