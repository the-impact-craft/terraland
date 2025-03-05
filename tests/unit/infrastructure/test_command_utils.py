import pytest
from io import StringIO
from terraland.infrastructure.shared.command_utils import process_stdout_stderr, clean_up_command_output
from terraland.infrastructure.shared.exceptions import CommandExecutionException


def test_process_stdout_simple():
    """Test processing simple stdout content"""
    stdout = StringIO("Hello\nWorld\n")
    stderr = StringIO("")

    output = list(process_stdout_stderr(stdout, stderr))
    assert output == ["Hello", "World"]


def test_process_stdout_with_input_prompt():
    """Test processing stdout with input prompt"""
    stdout = StringIO("Some output\nEnter a value: ")
    stderr = StringIO("")

    output = list(process_stdout_stderr(stdout, stderr))
    assert output == ["Some output", "Enter a value:", ""]


def test_process_stderr():
    """Test processing stderr content"""
    stdout = StringIO("")
    stderr = StringIO("Error message\nAnother error\n")

    with pytest.raises(CommandExecutionException) as exc_info:
        list(process_stdout_stderr(stdout, stderr))

    assert "Error message" in str(exc_info.value)
    assert "Another error" in str(exc_info.value)


def test_process_stdout_without_newline():
    """Test processing stdout content without trailing newline"""
    stdout = StringIO("Hello World")
    stderr = StringIO("")

    output = list(process_stdout_stderr(stdout, stderr))
    assert output == ["Hello World"]


def test_process_empty_streams():
    """Test processing empty stdout and stderr"""
    stdout = StringIO("")
    stderr = StringIO("")

    output = list(process_stdout_stderr(stdout, stderr))
    assert output == []


def test_process_mixed_output():
    """Test processing mixed stdout and stderr content"""
    stdout = StringIO("Standard output\nMore output\n")
    stderr = StringIO("Error occurred\n")

    with pytest.raises(CommandExecutionException) as exc_info:
        output = list(process_stdout_stderr(stdout, stderr))
        assert "Standard output" in output
        assert "More output" in output

    assert "Error occurred" in str(exc_info.value)


def test_clean_up_simple_ansi():
    """Test cleaning simple ANSI escape sequences"""
    text = "\x1b[31mRed Text\x1b[0m"
    cleaned = clean_up_command_output(text)
    assert cleaned == "Red Text"


def test_clean_up_multiple_ansi():
    """Test cleaning multiple ANSI escape sequences"""
    text = "\x1b[1mBold\x1b[31mRed\x1b[0m"
    cleaned = clean_up_command_output(text)
    assert cleaned == "BoldRed"


def test_clean_up_complex_ansi():
    """Test cleaning complex ANSI escape sequences"""
    text = "\x1b[38;2;255;0;0mRGB Red\x1b[0m"
    cleaned = clean_up_command_output(text)
    assert cleaned == "RGB Red"


def test_clean_up_no_ansi():
    """Test cleaning text without ANSI sequences"""
    text = "Plain text"
    cleaned = clean_up_command_output(text)
    assert cleaned == "Plain text"


def test_clean_up_with_whitespace():
    """Test cleaning text with whitespace"""
    text = "  \x1b[31mRed Text\x1b[0m  \n"
    cleaned = clean_up_command_output(text)
    assert cleaned == "Red Text"


def test_clean_up_empty_string():
    """Test cleaning empty string"""
    text = ""
    cleaned = clean_up_command_output(text)
    assert cleaned == ""


def test_process_stdout_large_content():
    """Test processing large stdout content"""
    large_content = "x" * 1000 + "\n" + "y" * 1000 + "\n"
    stdout = StringIO(large_content)
    stderr = StringIO("")

    output = list(process_stdout_stderr(stdout, stderr))
    assert len(output) == 2
    assert all(len(line) == 1000 for line in output)


def test_process_stderr_with_ansi():
    """Test processing stderr with ANSI sequences"""
    stdout = StringIO("")
    stderr = StringIO("\x1b[31mError\x1b[0m\n")

    with pytest.raises(CommandExecutionException) as exc_info:
        list(process_stdout_stderr(stdout, stderr))

    assert "Error" in str(exc_info.value)
    assert "\x1b[31m" not in str(exc_info.value)
