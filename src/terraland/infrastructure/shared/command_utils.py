from typing import IO, Generator
import re

from terraland.infrastructure.shared.exceptions import CommandExecutionException


def process_stdout_stderr(stdout: IO, stderr: IO) -> Generator[str, None, None]:
    """
    Processes the stdout and stderr streams from the Terraform command execution.

    This method processes the stdout and stderr streams from the Terraform command execution
    and writes the output to the TerraformCommandOutputScreen component.

    Parameters:
        stdout (IO): The stdout stream from the Terraform command execution
        stderr (IO): The stderr stream from the Terraform command execution
    """
    
    yield from process_stdout(stdout)
    yield from process_stderr(stderr)
    

def process_stdout(stdout: IO):
    """
    Processes the stdout stream from a command execution.

    Reads characters from the stdout stream one by one, accumulating them into lines.
    Yields each line after cleaning up the command output, either when a newline
    character is encountered or when a specific prompt is detected.
    
    Parameters:
        stdout (IO): The stdout stream from which to read the output.
        
    Yields:
        str: Each cleaned line from the stdout stream.
    """
    line = []

    for char in iter(lambda: stdout.read(1), ""):
        line.append(char)
        if char == "\n" or "Enter a value:" in ''.join(line):
            yield clean_up_command_output(''.join(line))
            line.clear()

    if line:
        yield clean_up_command_output(''.join(line))

def process_stderr(stderr: IO):
    """
    Processes the stderr stream from a command execution.

    Reads lines from the stderr stream, cleans up the command output,
    and yields each cleaned line. If any lines are processed, raises
    a CommandExecutionException with the accumulated error messages.

    Parameters:
        stderr (IO): The stderr stream from which to read the output.

    Yields:
        str: Each cleaned line from the stderr stream.
    
    Raises:
        CommandExecutionException: If any error messages are present in stderr.
    """
    exception = []
    for line in iter(stderr.readline, ""):
        if line:
            cleaned_line = clean_up_command_output(line)
            exception.append(cleaned_line)
            yield cleaned_line

    if exception:
        raise CommandExecutionException("\n".join(exception))


def clean_up_command_output(text: str):
    """Remove ANSI escape sequences from output."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text).strip()
