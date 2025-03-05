from dataclasses import dataclass

from terraland.domain.terraform.core.entities import ValidateSettings
from terraland.presentation.cli.messages.base_tf_action_request import BaseTfActionRequest


@dataclass
class ValidateActionRequest(BaseTfActionRequest):
    """
    Represents a request to validate the init settings.

    This class encapsulates data regarding the application of validate settings in a message.
    It is used for transmitting and processing validate-related instructions. The purpose of
    this class is to provide a structured format for handling validate settings in the application.

    """

    settings: ValidateSettings
