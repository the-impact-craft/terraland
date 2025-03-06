from pathlib import Path
import pytest
from unittest.mock import patch, Mock
import subprocess

from terraland.infrastructure.file_system.services import FileSystemService
from terraland.infrastructure.file_system.exceptions import FileSystemGrepException, ReadFileException, ListDirException
from terraland.domain.file_system.entities import SearchResultOutput, ListDirOutput


class TestFileSystemService:
    @pytest.mark.parametrize(
        "input_path,expected_type",
        [
            (lambda x: str(x), Path),
            (lambda x: x, Path),
        ],
    )
    def test_init(self, temp_dir, input_path, expected_type):
        """Test initialization with different path types"""

        service = FileSystemService(input_path(temp_dir))

        assert isinstance(service.work_dir, expected_type)
        assert service.work_dir == temp_dir

    def test_list_state_files_empty_directory(self, file_system_service):
        """Test listing state files in empty directory"""
        assert file_system_service.list_state_files() == []

    def test_list_state_files_with_files(self, file_system_service, temp_dir_with_files):
        """Test listing state files when files exist"""
        # Create test state files

        state_files = file_system_service.list_state_files()
        assert len(state_files) == 2
        assert "test1.tfstate" in state_files
        assert "subfolder/test2.tfstate" in state_files

    def test_grep_successful_search(self, file_system_service_with_grep_files):
        """Test successful grep search"""

        grep_results = file_system_service_with_grep_files._mocked_grep_results
        mock_result = Mock()
        mock_result.stdout = "\n".join(grep_results)
        mock_result.returncode = 0

        max_response_number = 1
        max_response_length = 100

        with patch("subprocess.run", return_value=mock_result):
            result = file_system_service_with_grep_files.grep("resource", max_response_number, max_response_length)
            assert isinstance(result, SearchResultOutput)
            assert result.total == len(grep_results)
            assert len(result.output) == min(max_response_number, len(grep_results))
            assert result.pattern == "resource"

    def test_grep_command_error(self, file_system_service):
        """Test grep command error handling"""
        error = subprocess.CalledProcessError(1, ["grep"], stderr=b"grep: error message")

        with patch("subprocess.run", side_effect=error):
            with pytest.raises(FileSystemGrepException) as exc_info:
                file_system_service.grep("pattern", 5, 100)
            assert "grep: error message" in str(exc_info.value)

    def test_grep_general_error(self, file_system_service):
        """Test grep general error handling"""
        with patch("subprocess.run", side_effect=Exception("Unexpected error")):
            with pytest.raises(FileSystemGrepException) as exc_info:
                file_system_service.grep("pattern", 5, 100)
            assert "Unexpected error" in str(exc_info.value)

    @pytest.mark.parametrize(
        "response_number,response_length",
        [
            (0, 10),  # Zero results
            (1, 0),  # Zero length
            (-1, 10),  # Negative results
            (10, -1),  # Negative length
            (999999, 999999),  # Very large limits
        ],
    )
    def test_grep_with_edge_case_limits(self, file_system_service_with_grep_files, response_number, response_length):
        """Test grep with edge case limits"""

        grep_results = file_system_service_with_grep_files._mocked_grep_results
        mock_result = Mock()
        mock_result.stdout = "\n".join(grep_results)
        mock_result.returncode = 0

        with patch("subprocess.run", return_value=mock_result):
            result = file_system_service_with_grep_files.grep("resource", response_number, response_length)
            if response_number <= 0:
                assert len(result.output) == 0
            if response_length <= 0:
                assert all(len(item.text) == 0 for item in result.output)

    def test_read(self, file_system_service):
        """Test reading file content"""
        file = Path(file_system_service.work_dir / "test.tf")
        file_content = "test content"
        file.write_text(file_content)

        content = file_system_service.read(file)
        assert content == file_content

    def test_wrong_path(self, file_system_service):
        """Test wrong path type"""
        with pytest.raises(ReadFileException):
            file_system_service.read("file")

    def test_not_existed_path(self, file_system_service):
        """Test non-existed path"""
        with pytest.raises(ReadFileException):
            file_system_service.read(Path("file"))

    def test_path_out_of_work_dir(self, file_system_service):
        """Test path out of work directory"""
        tmp_file = file_system_service.work_dir.parent / "test.tf"
        tmp_file.touch()
        with pytest.raises(ReadFileException):
            file_system_service.read(Path(tmp_file))
        tmp_file.unlink(missing_ok=True)

    def test_general_error(self, file_system_service):
        """Test general error"""
        (file_system_service.work_dir / "test.tf").touch()
        with patch("pathlib.Path.read_text", side_effect=Exception("Unexpected error")):
            with pytest.raises(ReadFileException):
                file_system_service.read(Path(file_system_service.work_dir / "test.tf"))

    def test_list_dir_with_valid_path(self, file_system_service, tmp_path):
        """Test listing directory with valid path"""
        directory = tmp_path / "test_dir"
        directory.mkdir()
        (directory / "file1.txt").touch()
        (directory / "file2.txt").touch()
        (directory / "subdir").mkdir()

        result = file_system_service.list_dir(path=directory, relative_paths=True)

        assert isinstance(result, ListDirOutput)
        assert len(result.files) == 2
        assert len(result.directories) == 1
        assert "file1.txt" in [f.name for f in result.files]
        assert "file2.txt" in [f.name for f in result.files]
        assert "subdir" in [d.name for d in result.directories]

    def test_list_dir_with_absolute_paths(self, file_system_service, tmp_path):
        """Test listing directory with absolute paths"""
        directory = tmp_path / "test_dir"
        directory.mkdir()
        (directory / "file.txt").touch()
        (directory / "subdir").mkdir()

        result = file_system_service.list_dir(path=directory, relative_paths=False)

        assert isinstance(result, ListDirOutput)
        assert len(result.files) == 1
        assert len(result.directories) == 1
        assert directory / "file.txt" in result.files
        assert directory / "subdir" in result.directories

    def test_list_dir_path_not_found(self, file_system_service):
        """Test listing directory with non-existing path"""
        non_existing_path = Path("/non/existing/path")

        with pytest.raises(ListDirException) as exc_info:
            file_system_service.list_dir(path=non_existing_path)

        assert "Directory not found" in str(exc_info.value)

    def test_list_dir_path_is_not_a_directory(self, file_system_service, tmp_path):
        """Test listing directory with a file path"""
        file_path = tmp_path / "file.txt"
        file_path.touch()

        with pytest.raises(ListDirException) as exc_info:
            file_system_service.list_dir(path=file_path)

        assert "Path is not a directory" in str(exc_info.value)

    def test_list_dir_path_outside_work_dir(self, file_system_service, tmp_path):
        """Test listing directory with path outside work directory"""
        outside_path = tmp_path.parent / "outside_dir"
        outside_path.mkdir()

        with pytest.raises(ListDirException) as exc_info:
            file_system_service.list_dir(path=outside_path)

        assert "Access denied: Path outside work directory" in str(exc_info.value)

    def test_list_dir_path_not_path_object(self, file_system_service):
        """Test listing directory with invalid path type"""
        invalid_path = "/invalid/path"

        with pytest.raises(ListDirException) as exc_info:
            file_system_service.list_dir(path=invalid_path)

        assert "Path must be a Path object" in str(exc_info.value)

    def test_access_denied(self, tmp_path, file_system_service):
        """Test access denied error"""
        directory = tmp_path / "test_dir"
        directory.mkdir()

        with patch("pathlib.Path.iterdir", side_effect=PermissionError("Access denied")):
            with pytest.raises(ListDirException) as exc_info:
                file_system_service.list_dir(path=directory)
            assert "Access denied" in str(exc_info.value)

    def test_general_exception(self, tmp_path, file_system_service):
        """Test access denied error"""
        directory = tmp_path / "test_dir"
        directory.mkdir()

        with patch("pathlib.Path.iterdir", side_effect=Exception("message")):
            with pytest.raises(ListDirException) as exc_info:
                file_system_service.list_dir(path=directory)
            assert "message" in str(exc_info.value)
