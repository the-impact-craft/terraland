import subprocess
from pathlib import Path

from terry.domain.file_system.entities import SearchResult, SearchResultOutput, ListDirOutput
from terry.domain.file_system.services import BaseFileSystemService
from terry.infrastructure.file_system.exceptions import (
    FileSystemGrepException,
    ReadFileException,
    ListDirException,
    CreateFileException,
    CreateDirException,
)


class FileSystemService(BaseFileSystemService):
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
            result = subprocess.run(command, capture_output=True, check=True)
            result = result.stdout.decode("utf-8").split("\n")
            result = [i.strip() for i in result if i.strip().startswith(str(self.work_dir))]
            # Remove the last empty line and the line that shows the total number of results
            total_search_result = len(result)
            result = [value.split(":", 2) for value in result[:result_limit]]
            result = [
                SearchResult(
                    text=value[2].strip()[:text_limit],
                    file_name=str(Path(value[0]).relative_to(self.work_dir)),
                    line=int(value[1]),
                )
                for value in result
                if len(value) == 3
            ]
            return SearchResultOutput(pattern=pattern, output=result, total=total_search_result)

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
        try:
            path.relative_to(self.work_dir)
        except ValueError:
            raise ReadFileException("Access denied: Path outside work directory")
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

    def create_file(self, path: Path) -> None:
        """
        Create a new file at the specified path.

        Args:
            path (Path): The path to the new file.

        Raises:
            CreateFileException: If the file creation operation fails.
        """
        try:
            path.relative_to(self.work_dir)
        except ValueError:
            raise CreateFileException("Access denied: Path outside work directory")
        try:
            if not path.parent.exists():
                path.parent.mkdir(parents=True)
            path.touch()
        except Exception as e:
            raise CreateFileException(f"Error creating file: {e}")

    def create_dir(self, path: Path) -> None:
        """
        Create a new directory at the specified path.

        Args:
            path (Path): The path to the new directory.

        Raises:
            CreateDirException: If the directory creation operation fails.
        """

        try:
            path.relative_to(self.work_dir)
        except ValueError:
            raise CreateDirException("Access denied: Path outside work directory")
        try:
            path.mkdir(parents=True)
        except Exception as e:
            raise CreateDirException(f"Error creating directory: {e}")
