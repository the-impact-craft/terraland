from enum import Enum
from typing import List, Literal

from terry.domain.terraform.core.entities import TerraformCommand


class CommandStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


DEFAULT_LANGUAGE: str = "python"

TERRAFORM_MAIN_ACTIONS: List[TerraformCommand] = [
    TerraformCommand("INIT", "init", "ctrl+t+i"),
    TerraformCommand("PLAN", "plan", "ctrl+t+p"),
    TerraformCommand("APPLY", "apply", "ctrl+t+a"),
    # TerraformCommand("DESTROY", "destroy", "ctrl+t+d"),
    TerraformCommand("VALIDATE", "validate", "ctrl+t+v"),
]

TERRAFORM_ADDITIONAL_ACTIONS: List[TerraformCommand] = [
    # TerraformCommand("CONSOLE", "console", "ctrl+t+c"),
    TerraformCommand("FORMAT", "fmt", "ctrl+t+f"),
    # TerraformCommand("FORCE_UNLOCK", "force-unlock", "ctrl+t+u"),
    # TerraformCommand("GET", "get", "ctrl+t+g"),
    # TerraformCommand("GRAPH", "graph", "ctrl+t+h"),
    # TerraformCommand("IMPORT", "import", "ctrl+t+b"),
    # TerraformCommand("LOGIN", "login", "ctrl+t+l"),
    # TerraformCommand("LOGOUT", "logout", "ctrl+t+k"),
    # TerraformCommand("METADATA", "metadata", "ctrl+t+m"),
    # TerraformCommand("OUTPUT", "output", "ctrl+t+o"),
    # TerraformCommand("PROVIDERS", "providers", "ctrl+t+e"),
    # TerraformCommand("REFRESH", "refresh", "ctrl+t+r"),
    # TerraformCommand("SHOW", "show", "ctrl+t+s"),
    # TerraformCommand("STATE", "state", "ctrl+t+y"),
    # TerraformCommand("TAINT", "taint", "ctrl+t+t"),
    # TerraformCommand("TEST", "test", "ctrl+t+j"),
    # TerraformCommand("UNTAINT", "untaint", "ctrl+t+w"),
    # TerraformCommand("VERSION", "version", "ctrl+t+n"),
    TerraformCommand("ABOUT", "about", "ctrl+shift+a", is_terraform_command=False),
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

SYSTEM_EVENTS_MONITORING_TIMEOUT = 5  # 5 seconds
