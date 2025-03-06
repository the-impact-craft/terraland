import shutil
import subprocess
from pathlib import Path

from terraland.domain.file_system.entities import SearchResult, SearchResultOutput, ListDirOutput
from terraland.domain.file_system.services import BaseFileSystemService
from terraland.infrastructure.file_system.exceptions import (
    FileSystemGrepException,
    ReadFileException,
    ListDirException,
    CreateFileException,
    CreateDirException,
    DeleteFileException,
    DeleteDirException,
    MoveFileException,
)


class FileSystemService(BaseFileSystemService):
    ACCESS_DENIED_ERROR = "Access denied: Path outside work directory"
    FILE_NOT_FOUND_ERROR = "File does not exist"
    MOVING_FILE_ERROR = "Moving file error"

    def __init__(self, work_dir: Path | str):
        """
        Initialize a Directory instance with the specified project directory.

        Parameters:
            directory (Path or str): The path to the project directory. If a string is provided,
            it will be converted to a Path object.

        Attributes:
            self.directory (Path): The normalized Path object representing the project directory.
        """
        self.work_dir = work_dir if isinstance(work_dir, Path) else Path(work_dir)

    def list_state_files(self) -> list[str]:
        """
        List all Terraform state files within the directory.

        Returns:
            list[str]: Relative paths to all .tfstate files found recursively in the directory.

        Example:
            directory = Directory('/path/to/project')
            state_files = directory.list_state_files()
            # Returns ['subfolder/main.tfstate', 'another/state.tfstate']
        """
        return [str(path.relative_to(self.work_dir)) for path in self.work_dir.rglob("*.tfstate")]

    def grep(self, pattern: str, result_limit: int, text_limit: int) -> SearchResultOutput:
        """
        Search for a pattern within all files in the project directory.

        Args:
            pattern (str): The search pattern to match within the files.
            result_limit (int): The maximum number of search results to return.
            text_limit (int): The maximum number of characters to return for each search

        Returns:
            SearchResultOutput: A data class containing the search results and the total number of matches.

        Notes:
            - Searches using the `grep` method of the `Directory` class
            - Formats results as tuples of (result_text, file_path_with_line_number)
            - Limits search results to first 5 matches
            - Truncates result text to first 100 characters

        Example:
            directory = Directory('/path/to/project')
            results = directory.grep('resource "aws_instance"')
            # Returns (b'file1.tf:12:resource "aws_instance"', b'', 0)

        """
        result_limit = max(result_limit, 0)
        text_limit = max(text_limit, 0)
        command = ["grep", "-nr", pattern, str(self.work_dir)]
        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            lines = result.stdout.splitlines()
            filtered_lines = [line for line in lines if line.startswith(str(self.work_dir))]
            total_search_result = len(filtered_lines)
            results = [
                SearchResult(
                    text=value[2].strip()[:text_limit],
                    file_name=str(Path(value[0]).relative_to(self.work_dir)),
                    line=int(value[1]),
                )
                for value in (line.split(":", 2) for line in filtered_lines[:result_limit])
                if len(value) == 3
            ]
            return SearchResultOutput(pattern=pattern, output=results, total=total_search_result)

        except subprocess.CalledProcessError as e:
            raise FileSystemGrepException(e.stderr.decode())
        except Exception as e:
            raise FileSystemGrepException(str(e))

    def read(self, path: Path) -> str:
        """
        Reads and processes the contents of a file located at the specified path.

        This method will attempt to open the file, read its content, and perform
        any necessary processing on the data. It assumes that the file is in
        a format appropriate for the specific application logic and that the
        given path is accessible.

        Args:
            path (Path): The path to the file to read.

        Returns:
            str: The processed data extracted from the file.

        Raises:
            ReadFileException: An error occurred during the file read operation.
        """

        if not isinstance(path, Path):
            raise ReadFileException("file_path must be a Path object")
        if not path.exists():
            raise ReadFileException(f"File not found: {path}")
        self.validate_path_within_work_dir(path, ReadFileException)
        try:
            return path.read_text()
        except Exception as e:
            raise ReadFileException(f"Error reading file: {e}")

    def list_dir(self, path: Path, relative_paths: bool = False) -> ListDirOutput:
        """
        List all files and directories within the specified directory.

        Args:
            path (Path): The path to the directory.
            relative_paths (bool): Whether to return relative paths or full paths.

        Returns:
             ListDirOutput: A data class containing the list of files and directories within the specified path.
                - files (list[Path]): Sorted list of file paths
                - directories (list[Path]): Sorted list of directory paths

        Raises:
            ListDirException: If the path is invalid, directory doesn't exist, or path is not a directory.

        """
        if not isinstance(path, Path):
            raise ListDirException("Path must be a Path object")
        if not path.exists():
            raise ListDirException(f"Directory not found: {path}")
        if not path.is_dir():
            raise ListDirException(f"Path is not a directory: {path}")
        try:
            path.relative_to(self.work_dir)
        except ValueError:
            raise ListDirException("Access denied: Path outside work directory")
        try:
            files = []
            directories = []

            for entry in path.iterdir():
                target = files if entry.is_file() else directories
                target.append(entry.relative_to(path) if relative_paths else entry)
            return ListDirOutput(files=files, directories=directories)
        except PermissionError as e:
            raise ListDirException(f"Access denied: {e}")
        except Exception as e:
            raise ListDirException(f"Error listing directory: {e}")

    def create_file(self, path: Path, content: str | None = None) -> None:
        """
        Create a new file at the specified path.

        Args:
            path (Path): The path to the new file.
            content (str | None): Optional file content

        Raises:
            CreateFileException: If the file creation operation fails.
        """
        self.validate_path_within_work_dir(path, CreateFileException)
        try:
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            if not content:
                path.touch()
            else:
                path.write_text(content)
        except Exception as e:
            raise CreateFileException(f"Error creating file: {e}")

    def move(self, src_path: Path, dest_path: Path) -> None:
        """
        Moves a file or directory from the source path to the destination path.
        This operation is performed while preserving metadata, ensuring the
        complete transfer of the resource from its original location to the
        specified target location.

        Arguments:
            src_path (Path): The source path of the file or directory to be moved.
            dest_path (Path): The destination path where the file or directory should be moved.
        """

        self.validate_path_within_work_dir(src_path, MoveFileException)
        self.validate_path_within_work_dir(dest_path, MoveFileException)

        try:
            shutil.move(src_path, dest_path)
        except FileNotFoundError as ex:
            raise MoveFileException(f"{self.FILE_NOT_FOUND_ERROR}: {ex}")
        except PermissionError as ex:
            raise MoveFileException(f"{self.ACCESS_DENIED_ERROR}: {ex}")
        except Exception as ex:
            raise MoveFileException(f"{self.MOVING_FILE_ERROR}: {ex}")

    def create_dir(self, path: Path) -> None:
        """
        Create a new directory at the specified path.

        Args:
            path (Path): The path to the new directory.

        Raises:
            CreateDirException: If the directory creation operation fails.
        """
        self.validate_path_within_work_dir(path, CreateDirException)
        try:
            path.mkdir(parents=True)
        except Exception as e:
            raise CreateDirException(f"Error creating directory: {e}")

    def delete_file(self, path: Path) -> None:
        """
        Delete the file at the specified path.

        Args:
            path (Path): The path to the file to delete.

        Raises:
            DeleteFileException: If the file deletion operation fails.
        """
        self.validate_path_within_work_dir(path, DeleteFileException)
        try:
            path.unlink()
        except Exception as e:
            raise DeleteFileException(f"Error deleting file: {e}")

    def delete_dir(self, path: Path) -> None:
        """
        Deletes the specified directory and all of its contents recursively.

        This method ensures that the directory specified by the given path is
        removed completely. Only applicable for writable directories. If the
        path does not exist or is not a directory, the method does nothing.

        Args:
            path (Path): The path to the directory to delete.
        """
        self.validate_path_within_work_dir(path, DeleteDirException)

        try:
            shutil.rmtree(path, ignore_errors=True)
        except Exception as e:
            raise DeleteDirException(f"Error deleting directory: {e}")

    def validate_path_within_work_dir(self, path: Path, exception_class: type) -> None:
        """Validates if a path is within the working directory."""
        try:
            path.relative_to(self.work_dir)
        except ValueError:
            raise exception_class(self.ACCESS_DENIED_ERROR)
