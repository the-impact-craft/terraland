from pathlib import Path
from terraland.infrastructure.shared.command_process_context_manager import CommandProcessContextManager


def test_successful_command_execution(operation_system_service):
    """Test successful command execution and output capture"""
    with CommandProcessContextManager(["echo", "hello"], operation_system_service) as (stdin, stdout, stderr):
        # Read output
        output = stdout.read()
        assert "hello" in output

        # Verify no errors
        assert stderr.read() == ""


def test_command_with_error(operation_system_service):
    """Test command that returns error"""
    with CommandProcessContextManager(["ls", "nonexistent_directory"], operation_system_service) as (
        stdin,
        stdout,
        stderr,
    ):
        # Verify error output
        error_output = stderr.read()
        assert "No such file or directory" in error_output


def test_command_with_working_directory(operation_system_service):
    """Test command execution in specific working directory"""
    # Create a temporary directory and file
    temp_dir = Path("test_dir")
    temp_dir.mkdir(exist_ok=True)
    temp_file = temp_dir / "test.txt"
    temp_file.write_text("test content")

    try:
        with CommandProcessContextManager(["ls"], operation_system_service, cwd=str(temp_dir)) as (
            stdin,
            stdout,
            stderr,
        ):
            output = stdout.read()
            assert "test.txt" in output
    finally:
        # Cleanup
        temp_file.unlink()
        temp_dir.rmdir()


def test_command_with_environment_variables(operation_system_service):
    """Test command execution with environment variables"""
    env_vars = {"TEST_VAR": "test_value"}
    with CommandProcessContextManager(["env"], operation_system_service, env_vars=env_vars) as (stdin, stdout, stderr):
        output = stdout.read()
        assert "TEST_VAR=test_value" in output


def test_command_with_input(operation_system_service):
    """Test command with stdin input"""
    with CommandProcessContextManager(["cat"], operation_system_service) as (stdin, stdout, stderr):
        stdin.write("hello\n")
        stdin.flush()
        stdin.close()
        output = stdout.read()
        assert "hello" in output


def test_process_termination(operation_system_service):
    """Test process termination"""
    manager = CommandProcessContextManager(["sleep", "10"], operation_system_service)
    with manager as (stdin, stdout, stderr):
        # Verify process exists
        assert manager.process is not None
        assert manager.process.poll() is None  # Process is running

    # After context exit, process should be terminated
    assert manager.process is None


def test_multiple_context_entries(operation_system_service):
    """Test multiple entries to the context manager"""
    manager = CommandProcessContextManager(["echo", "hello"], operation_system_service)

    # First entry
    with manager as (stdin1, stdout1, stderr1):
        output1 = stdout1.read()
        assert "hello" in output1

    # Second entry should work with new process
    with manager as (stdin2, stdout2, stderr2):
        output2 = stdout2.read()
        assert "hello" in output2


def test_error_handling(operation_system_service):
    """Test error handling within context"""

    class CustomError(Exception):
        pass

    manager = CommandProcessContextManager(["echo", "hello"], operation_system_service)
    try:
        with manager as (stdin, stdout, stderr):
            raise CustomError("Test error")
    except CustomError:
        # Process should be cleaned up
        assert manager.process is None
        assert manager.error is not None


def test_text_mode_output(operation_system_service):
    """Test text mode output (strings instead of bytes)"""
    with CommandProcessContextManager(["echo", "hello"], operation_system_service) as (stdin, stdout, stderr):
        output = stdout.read()
        assert isinstance(output, str)  # Should be string, not bytes
        assert "hello" in output


def test_cleanup_on_exception(operation_system_service):
    """Test cleanup when an exception occurs"""
    manager = CommandProcessContextManager(["sleep", "10"], operation_system_service)
    try:
        with manager as (stdin, stdout, stderr):
            raise KeyboardInterrupt()
    except KeyboardInterrupt:
        pass

    # Verify cleanup occurred
    assert manager.process is None
