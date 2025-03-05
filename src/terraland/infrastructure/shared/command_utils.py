import re

from terraland.infrastructure.shared.exceptions import CommandExecutionException


def process_stdout_stderr(stdout, stderr):
    """
    Processes the stdout and stderr streams from the Terraform command execution.

    This method processes the stdout and stderr streams from the Terraform command execution
    and writes the output to the TerraformCommandOutputScreen component.

    Parameters:
        stdout (IO): The stdout stream from the Terraform command execution
        stderr (IO): The stderr stream from the Terraform command execution
    """
    exception = []
    line = ""
    for char in iter(lambda: stdout.read(1), ""):
        line += char
        if char == "\n" or "Enter a value:" in line:
            line = clean_up_command_output(line)
            yield line
            line = ""
    if line:
        line = clean_up_command_output(line)
        yield line

    for line in iter(stderr.readline, ""):
        if not line:
            continue
        line = clean_up_command_output(line)
        exception.append(line)
        yield line
    if exception:
        raise CommandExecutionException("\n".join(exception))


def clean_up_command_output(text: str):
    """Remove ANSI escape sequences from output."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text).strip()
