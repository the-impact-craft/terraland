from terraland.domain.terraform.core.entities import PlanSettings


class TerraformPlanCommandBuilder:
    def __init__(self):
        self._command = ["terraform", "plan"]

    def set_refresh_only(self) -> "TerraformPlanCommandBuilder":
        self._command.append("-refresh-only")
        return self

    def set_destroy(self) -> "TerraformPlanCommandBuilder":
        self._command.append("-destroy")
        return self

    def set_no_refresh(self) -> "TerraformPlanCommandBuilder":
        self._command.append("-refresh=false")
        return self

    def add_inline_var(self, name: str, value: str) -> "TerraformPlanCommandBuilder":
        self._command.extend(["-var", f"{name}={value}"])
        return self

    def add_var_file(self, file: str) -> "TerraformPlanCommandBuilder":
        self._command.extend(["-var-file", file])
        return self

    def add_out(self, out: str) -> "TerraformPlanCommandBuilder":
        self._command.extend(["-out", out])
        return self

    def build(self) -> list[str]:
        return self._command

    def build_from_settings(self, settings: PlanSettings) -> list[str]:
        if settings.refresh_only:
            self.set_refresh_only()
        if settings.destroy:
            self.set_destroy()
        if settings.norefresh:
            self.set_no_refresh()
        if settings.inline_vars:
            for var in settings.inline_vars:
                if not var.name or not var.value:
                    continue
                self.add_inline_var(var.name, var.value)
        if settings.var_files:
            for var_file in settings.var_files:
                self.add_var_file(var_file)
        if settings.out:
            self.add_out(settings.out)
        return self.build()