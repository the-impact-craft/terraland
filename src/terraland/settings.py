from enum import Enum
from typing import List, Literal

from terraland.domain.terraform.core.entities import TerraformCommand


class CommandStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


STATUS_TO_COLOR: dict[CommandStatus, str] = {
    CommandStatus.SUCCESS: "green",
    CommandStatus.ERROR: "red",
}

STATUS_TO_ICON: dict[CommandStatus, str] = {
    CommandStatus.SUCCESS: "🟢",
    CommandStatus.ERROR: "🔴",
}

DEFAULT_LANGUAGE: str = "python"

TERRAFORM_MAIN_ACTIONS: List[TerraformCommand] = [
    TerraformCommand("INIT", "init", "ctrl+shift+i"),
    TerraformCommand("PLAN", "plan", "ctrl+shift+p"),
    TerraformCommand("APPLY", "apply", "ctrl+shift+a"),
    # TerraformCommand("DESTROY", "destroy", "ctrl+shift+d"),
    TerraformCommand("VALIDATE", "validate", "ctrl+shift+v"),
]

TERRAFORM_ADDITIONAL_ACTIONS: List[TerraformCommand] = [
    # TerraformCommand("CONSOLE", "console", "ctrl+shift+c"),
    TerraformCommand("FORMAT", "fmt", "ctrl+shift+f"),
    # TerraformCommand("FORCE_UNLOCK", "force-unlock", "ctrl+shift+u"),
    # TerraformCommand("GET", "get", "ctrl+shift+g"),
    # TerraformCommand("GRAPH", "graph", "ctrl+shift+h"),
    # TerraformCommand("IMPORT", "import", "ctrl+shift+b"),
    # TerraformCommand("LOGIN", "login", "ctrl+shift+l"),
    # TerraformCommand("LOGOUT", "logout", "ctrl+shift+k"),
    # TerraformCommand("METADATA", "metadata", "ctrl+shift+m"),
    # TerraformCommand("OUTPUT", "output", "ctrl+shift+o"),
    # TerraformCommand("PROVIDERS", "providers", "ctrl+shift+e"),
    # TerraformCommand("REFRESH", "refresh", "ctrl+shift+r"),
    # TerraformCommand("SHOW", "show", "ctrl+shift+s"),
    # TerraformCommand("STATE", "state", "ctrl+shift+y"),
    # TerraformCommand("TAINT", "taint", "ctrl+shift+t"),
    # TerraformCommand("TEST", "test", "ctrl+shift+j"),
    # TerraformCommand("UNTAINT", "untaint", "ctrl+shift+w"),
    # TerraformCommand("VERSION", "version", "ctrl+shift+v"),
    TerraformCommand("ABOUT", "about", "ctrl+i", is_terraform_command=False),
]

SEVERITY_LEVEL_INFORMATION: Literal["information"] = "information"
SEVERITY_LEVEL_ERROR: Literal["error"] = "error"

ANIMATION_ENABLED: bool = True
ANIMATION_SPEED: float = 0.3  # frame per 0.3 seconds
DOUBLE_CLICK_THRESHOLD = 1.5  # seconds
DEFAULT_THEME: str = "github-dark"

# ------------------------------------------------------------------------------------------
# Terraform commands timeouts
# ------------------------------------------------------------------------------------------

TERRAFORM_VERSION_TIMEOUT: int = 30  # 30 seconds
TERRAFORM_FORMAT_TIMEOUT: int = 300  # 5 minutes
TERRAFORM_INIT_TIMEOUT: int = 600  # 10 minutes
TERRAFORM_PLAN_TIMEOUT: int = 900  # 15 minutes
TERRAFORM_APPLY_TIMEOUT: int = 1200  # 20 minutes
TERRAFORM_DESTROY_TIMEOUT: int = 1200  # 20 minutes
TERRAFORM_VALIDATE_TIMEOUT: int = 600  # 10 minutes
TERRAFORM_CONSOLE_TIMEOUT: int = 600  # 10 minutes

# ------------------------------------------------------------------------------------------
# Search settings
# ------------------------------------------------------------------------------------------

MAX_RESULTS: int = 20
MAX_TEXT_LENGTH: int = 100

# ------------------------------------------------------------------------------------------
# Icons
# ------------------------------------------------------------------------------------------
DIRECTORY_ICON = "📁"
FILE_ICON = "📄"

# ------------------------------------------------------------------------------------------
# Application settings
# ------------------------------------------------------------------------------------------

# List of prefixes used to filter environment variables in the plan screen.
# - TF_VAR: Terraform variables
# - AWS: AWS credentials and configuration
# - ARM: Azure Resource Manager credentials and configuration
ENV_VARS_PREFIXES = [
    "TF_VAR",
    "AWS",
    "ARM",
]

MIN_SECTION_DIMENSION = 10  # Minimum width/height for components

SYSTEM_EVENTS_MONITORING_TIMEOUT = 1  # 1 second

MAX_TABS_HOT_KEY = 9
