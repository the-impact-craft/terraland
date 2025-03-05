from pathlib import Path

from terraland.domain.terraform.core.entities import PlanSettings, InitSettings, ValidateSettings, ApplySettings, Variable
from terraland.infrastructure.terraform.core.command_builders.terraform_apply_command_builder import \
    TerraformApplyCommandBuilder
from terraland.infrastructure.terraform.core.command_builders.terraform_init_command_builder import \
    TerraformInitCommandBuilder
from terraland.infrastructure.terraform.core.command_builders.terraform_plan_command_builder import \
    TerraformPlanCommandBuilder
from terraland.infrastructure.terraform.core.command_builders.terraform_validate_command_builder import \
    TerraformValidateCommandBuilder


class TestTerraformPlanCommandBuilder:
    def test_plan_command_with_minimal_settings(self):
        """Test plan command with minimal settings"""
        settings = PlanSettings()
        builder = TerraformPlanCommandBuilder()
        command = builder.build_from_settings(settings)

        assert command == ["terraform", "plan"]

    def test_plan_command_with_refresh_only(self):
        """Test plan command with refresh-only flag"""
        settings = PlanSettings(refresh_only=True)
        builder = TerraformPlanCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-refresh-only" in command

    def test_plan_command_with_destroy(self):
        """Test plan command with destroy flag"""
        settings = PlanSettings(destroy=True)
        builder = TerraformPlanCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-destroy" in command

    def test_plan_command_with_no_refresh(self):
        """Test plan command with no refresh flag"""
        settings = PlanSettings(norefresh=True)
        builder = TerraformPlanCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-refresh=false" in command

    def test_plan_command_with_inline_vars(self):
        """Test plan command with inline variables"""
        settings = PlanSettings(
            inline_vars=[Variable(name="region", value="us-east-1"), Variable(name="env", value="prod")]
        )
        builder = TerraformPlanCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-var" in command
        assert "region=us-east-1" in command
        assert "env=prod" in command

    def test_plan_command_with_var_files(self):
        """Test plan command with variable files"""
        settings = PlanSettings(var_files=["prod.tfvars", "common.tfvars"])
        builder = TerraformPlanCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-var-file" in command
        assert "prod.tfvars" in command
        assert "common.tfvars" in command


class TestTerraformInitCommandBuilder:
    def test_init_command_with_minimal_settings(self):
        """Test init command with minimal settings"""
        settings = InitSettings()
        builder = TerraformInitCommandBuilder()
        command = builder.build_from_settings(settings)

        assert command == ["terraform", "init"]

    def test_init_command_with_backend_config(self):
        """Test init command with backend configuration"""
        settings = InitSettings(backend_config={"key": "value", "region": "us-east-1"})
        builder = TerraformInitCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-backend-config" in command
        assert "key=value" in command
        assert "region=us-east-1" in command

    def test_init_command_with_backend_config_path(self):
        """Test init command with backend config file"""
        settings = InitSettings(backend_config_path=["config1.hcl", "config2.hcl"])
        builder = TerraformInitCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-backend-config" in command
        assert "config1.hcl" in command
        assert "config2.hcl" in command

    def test_init_command_with_plugin_dir(self):
        """Test init command with plugin directory"""
        settings = InitSettings(plugin_dir=["plugins1", "plugins2"])
        builder = TerraformInitCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-plugin-dir" in command
        assert "plugins1" in command
        assert "plugins2" in command

    def test_init_command_with_test_directory(self):
        """Test init command with test directory"""
        settings = InitSettings(test_directory=["tests1", "tests2"])
        builder = TerraformInitCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-test-directory" in command
        assert "tests1" in command
        assert "tests2" in command

    def test_init_command_with_all_flags(self):
        """Test init command with all boolean flags"""
        settings = InitSettings(
            disable_backend=True,
            force_copy=True,
            disable_download=True,
            disable_input=True,
            disable_hold_lock=True,
            reconfigure=True,
            migrate_state=True,
            upgrade=True,
            ignore_remote_version=True,
        )
        builder = TerraformInitCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-backend=false" in command
        assert "-force-copy" in command
        assert "-get=false" in command
        assert "-input=false" in command
        assert "-lock=false" in command
        assert "-reconfigure" in command
        assert "-migrate-state" in command
        assert "-upgrade" in command
        assert "-ignore-remote-version" in command


class TestTerraformValidateCommandBuilder:
    def test_validate_command_with_minimal_settings(self):
        """Test validate command with minimal settings"""
        settings = ValidateSettings()
        builder = TerraformValidateCommandBuilder()
        command = builder.build_from_settings(settings)

        assert command == ["terraform", "validate"]

    def test_validate_command_with_no_tests(self):
        """Test validate command with no-tests flag"""
        settings = ValidateSettings(no_tests=True)
        builder = TerraformValidateCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-no-tests" in command

    def test_validate_command_with_test_directory(self):
        """Test validate command with test directory"""
        settings = ValidateSettings(test_directory=["tests1", "tests2"])
        builder = TerraformValidateCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-test-directory" in command
        assert "tests1" in command
        assert "tests2" in command


class TestTerraformApplyCommandBuilder:
    def test_apply_command_with_minimal_settings(self):
        """Test apply command with minimal settings"""
        settings = ApplySettings()
        builder = TerraformApplyCommandBuilder()
        command = builder.build_from_settings(settings)

        assert command == ["terraform", "apply"]

    def test_apply_command_with_auto_approve(self):
        """Test apply command with auto-approve"""
        settings = ApplySettings(auto_approve=True)
        builder = TerraformApplyCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-auto-approve" in command

    def test_apply_command_with_backup_settings(self):
        """Test apply command with backup settings"""
        settings = ApplySettings(backup=Path("backup.tfstate"))
        builder = TerraformApplyCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-backup" in command
        assert "backup.tfstate" in command

    def test_apply_command_with_disable_backup(self):
        """Test apply command with disabled backup"""
        settings = ApplySettings(disable_backup=True)
        builder = TerraformApplyCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-backup=-" in command

    def test_apply_command_with_state_settings(self):
        """Test apply command with state settings"""
        settings = ApplySettings(state=Path("current.tfstate"), state_out=Path("output.tfstate"))
        builder = TerraformApplyCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-state" in command
        assert "current.tfstate" in command
        assert "-state-out" in command
        assert "output.tfstate" in command

    def test_apply_command_with_all_flags(self):
        """Test apply command with all boolean flags"""
        settings = ApplySettings(auto_approve=True, destroy=True, disable_backup=True, disable_lock=True, input=True)
        builder = TerraformApplyCommandBuilder()
        command = builder.build_from_settings(settings)

        assert "-auto-approve" in command
        assert "-destroy" in command
        assert "-backup=-" in command
        assert "-lock=false" in command
        assert "-input" in command
