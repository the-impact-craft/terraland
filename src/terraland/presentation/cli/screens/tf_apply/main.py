from typing import List

from textual import on, events
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll, Horizontal
from textual.widget import Widget
from textual.widgets import Static, Rule

from terraland.domain.operation_system.entities import Variable
from terraland.domain.terraform.core.entities import TerraformApplySettingsAttributes, ApplySettings
from terraland.presentation.cli.commands_descriptions import (
    APPLY_DESCRIPTION,
    APPLY_AUTO_APPROVE_DESCRIPTION,
    APPLY_DESTROY_DESCRIPTION,
    APPLY_INPUT_DESCRIPTION,
    APPLY_DISABLE_BACKUP_DESCRIPTION,
    APPLY_BACKUP_DESCRIPTION,
    APPLY_STATE_OUT_DESCRIPTION,
    APPLY_STATE_DESCRIPTION,
    APPLY_DISABLE_LOCK_DESCRIPTION,
    APPLY_PLAN_DESCRIPTION,
    APPLY_ENV_VAR_DESCRIPTION,
    APPLY_INLINE_VAR_DESCRIPTION,
    APPLY_VAR_FILE_DESCRIPTION,
)

from terraland.presentation.cli.utils import get_unique_id
from terraland.presentation.cli.widgets.buttons.add_key_value_button import AddKeyValueButton
from terraland.presentation.cli.widgets.buttons.open_file_navigator_modal_button import FileNavigatorModalButton
from terraland.presentation.cli.widgets.form.checkbox_settings_block import CheckboxSettingBlock
from terraland.presentation.cli.widgets.form.collapsible_info_settings_block import CollapsibleInfoBlock
from terraland.presentation.cli.widgets.form.key_value_block import KeyValueBlock
from terraland.presentation.cli.widgets.form.text_input_block import TextInputBlock
from terraland.presentation.cli.widgets.modal_control_label import ModalControlLabel
from terraland.presentation.cli.screens.base.base_tf_settings_screen import BaseTfSettingsModalScreen
from terraland.presentation.cli.screens.file_system_navigation.main import FileSystemSelectionValidationRule


class ApplySettingsScreenControlLabel(ModalControlLabel):
    """A clickable label that emits an event when clicked."""


class ApplySettingsScreen(BaseTfSettingsModalScreen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]
    CONTAINER_ID: str = "apply_settings"
    CSS_PATH = "styles.tcss"

    def __init__(self, env_vars: List[Variable] | None = None, *args, **kwargs):
        self.env_vars = env_vars or []
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        with Container(id=self.CONTAINER_ID):
            yield Static(APPLY_DESCRIPTION, id="about_apply")

            with VerticalScroll(id="settings"):
                yield Rule()

                yield CheckboxSettingBlock(
                    TerraformApplySettingsAttributes.AUTO_APPROVE, "Auto approve", APPLY_AUTO_APPROVE_DESCRIPTION
                )

                yield CheckboxSettingBlock(
                    TerraformApplySettingsAttributes.DESTROY, "Destroy", APPLY_DESTROY_DESCRIPTION
                )

                yield CheckboxSettingBlock(
                    TerraformApplySettingsAttributes.DISABLE_BACKUP, "Disable backup", APPLY_DISABLE_BACKUP_DESCRIPTION
                )

                yield CheckboxSettingBlock(
                    TerraformApplySettingsAttributes.DISABLE_LOCK, "Disable lock", APPLY_DISABLE_LOCK_DESCRIPTION
                )

                yield CheckboxSettingBlock(
                    TerraformApplySettingsAttributes.INPUT, "Ask for input for variables", APPLY_INPUT_DESCRIPTION
                )

                yield Rule()
                yield CollapsibleInfoBlock(
                    "env_vars",
                    "Environment variables:",
                    APPLY_ENV_VAR_DESCRIPTION,
                )
                with Widget(id=TerraformApplySettingsAttributes.ENV_VARS):
                    for env_var in self.env_vars:
                        uuid = get_unique_id()
                        yield KeyValueBlock(
                            key=env_var.name,
                            value=env_var.value,
                            id=uuid,
                            show_view_button=True,
                            is_password=True,
                        )

                    yield AddKeyValueButton(
                        content="+ Add Environment Variable",
                        section_id=TerraformApplySettingsAttributes.ENV_VARS,
                        id="add_env_var_button",
                    )

                yield Rule()
                yield CollapsibleInfoBlock(
                    "inline_variables",
                    "Inline variables:",
                    APPLY_INLINE_VAR_DESCRIPTION,
                )
                with Widget(id=TerraformApplySettingsAttributes.INLINE_VARS):
                    yield AddKeyValueButton(
                        content="+ Add Inline Variable", section_id="inline_vars", id="add_inline_var_button"
                    )

                yield Rule()
                yield CollapsibleInfoBlock(
                    "var_files",
                    "Variables Files:",
                    APPLY_VAR_FILE_DESCRIPTION,
                )
                with Widget(id=TerraformApplySettingsAttributes.VAR_FILES):
                    yield FileNavigatorModalButton(
                        content="+ Add Variables File",
                        id="add_var_file_button",
                        section_id=TerraformApplySettingsAttributes.VAR_FILES,
                        validation_rules=[
                            FileSystemSelectionValidationRule(
                                action=lambda path: path.is_file(), error_message="Selected path is not a file"
                            )
                        ],
                    )
                yield Rule()

                yield TextInputBlock(
                    TerraformApplySettingsAttributes.BACKUP,
                    "Backup path",
                    APPLY_BACKUP_DESCRIPTION,
                    id=TerraformApplySettingsAttributes.BACKUP,
                )
                yield TextInputBlock(
                    TerraformApplySettingsAttributes.STATE_OUT,
                    "State out path",
                    APPLY_STATE_OUT_DESCRIPTION,
                    id=TerraformApplySettingsAttributes.STATE_OUT,
                )

                yield Rule()
                yield CollapsibleInfoBlock("state", "State path", APPLY_STATE_DESCRIPTION)
                with Widget(id=TerraformApplySettingsAttributes.STATE):
                    yield FileNavigatorModalButton(
                        content="+ State file path",
                        id="add_state_path",
                        section_id=TerraformApplySettingsAttributes.STATE,
                        validation_rules=[
                            FileSystemSelectionValidationRule(
                                action=lambda path: path.is_file(), error_message="Selected path is not a file"
                            )
                        ],
                    )

                yield Rule()
                yield CollapsibleInfoBlock("plan", "Plan path", APPLY_PLAN_DESCRIPTION)
                with Widget(id=TerraformApplySettingsAttributes.PLAN):
                    yield FileNavigatorModalButton(
                        content="+ Plan file path",
                        id="add_plan_path",
                        section_id=TerraformApplySettingsAttributes.PLAN,
                        validation_rules=[
                            FileSystemSelectionValidationRule(
                                action=lambda path: path.is_file(), error_message="Selected path is not a file"
                            )
                        ],
                    )

            yield Horizontal(
                ApplySettingsScreenControlLabel("Close", name="close", id="close", classes="button"),
                ApplySettingsScreenControlLabel("Apply", name="apply", id="apply", classes="button"),
                id="controls",
            )

    def on_mount(self, _: events.Mount) -> None:
        self.query_one(f"#{self.CONTAINER_ID}").border_title = "Apply Settings"

    @on(ApplySettingsScreenControlLabel.Close)
    def on_close(self, _: ApplySettingsScreenControlLabel.Close):
        self.dismiss(None)

    @on(ApplySettingsScreenControlLabel.Apply)
    def on_apply(self, _: ApplySettingsScreenControlLabel.Apply):
        result = self._initialize_result()

        checkbox_settings = self.process_checkbox_settings(
            [
                TerraformApplySettingsAttributes.AUTO_APPROVE,
                TerraformApplySettingsAttributes.DESTROY,
                TerraformApplySettingsAttributes.DISABLE_BACKUP,
                TerraformApplySettingsAttributes.DISABLE_LOCK,
                TerraformApplySettingsAttributes.INPUT,
            ],
        )

        paths_settings = self.process_files(
            [
                TerraformApplySettingsAttributes.STATE,
                TerraformApplySettingsAttributes.PLAN,
                TerraformApplySettingsAttributes.VAR_FILES,
            ]
        )

        key_value_settings = self.process_key_value_settings(
            [
                TerraformApplySettingsAttributes.ENV_VARS,
                TerraformApplySettingsAttributes.INLINE_VARS,
            ],
        )

        text_input_settings = self.process_text_inputs(
            [
                TerraformApplySettingsAttributes.BACKUP,
                TerraformApplySettingsAttributes.STATE_OUT,
            ]
        )

        result.update(
            {
                **paths_settings,
                **checkbox_settings,
                **key_value_settings,
                **text_input_settings,
            }
        )

        failed_settings = [setting for setting, value in result.items() if value is None]
        if failed_settings:
            self.notify(f"Failed to process settings: {', '.join(failed_settings)}", severity="error")
            return

        settings = ApplySettings(**result)
        self.dismiss(settings)

    def _initialize_result(self) -> dict:
        """Initialize the result dictionary with default values."""
        return {
            TerraformApplySettingsAttributes.AUTO_APPROVE: None,
            TerraformApplySettingsAttributes.DESTROY: None,
            TerraformApplySettingsAttributes.DISABLE_BACKUP: None,
            TerraformApplySettingsAttributes.DISABLE_LOCK: None,
            TerraformApplySettingsAttributes.INPUT: None,
            TerraformApplySettingsAttributes.BACKUP: None,
            TerraformApplySettingsAttributes.STATE: None,
            TerraformApplySettingsAttributes.STATE_OUT: None,
            TerraformApplySettingsAttributes.ENV_VARS: [],
            TerraformApplySettingsAttributes.INLINE_VARS: [],
            TerraformApplySettingsAttributes.VAR_FILES: [],
        }
