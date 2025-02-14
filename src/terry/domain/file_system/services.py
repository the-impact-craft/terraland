import abc
from pathlib import Path

from terry.domain.file_system.entities import SearchResultOutput, ListDirOutput


class BaseFileSystemService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def list_state_files(self):
        """
        List all Terraform state files within the directory.

        Returns:
            list[str]: Relative paths to all .tfstate files found recursively in the directory.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def grep(self, pattern: str, result_limit: int, text_limit: int) -> SearchResultOutput:
        """
        Search for a pattern within all files in the project directory.

        Args:
            pattern (str): The search pattern to match within the files.
            result_limit (int): The maximum number of search results to return.
            text_limit (int): The maximum number of characters to return for each search

        Returns:
            SearchResultOutput: A data class containing the search results and the total number of matches.
        """
        raise NotImplementedError

    @abc.abstractmethod
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
        raise NotImplementedError

    @abc.abstractmethod
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
        raise NotImplementedError

    @abc.abstractmethod
    def create_file(self, path: Path) -> None:
        """
        Create a new file at the specified path.

        Args:
            path (Path): The path to the new file.

        Raises:
            CreateFileException: If the file creation operation fails.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def create_dir(self, path: Path) -> None:
        """
        Create a new directory at the specified path.

        Args:
            path (Path): The path to the new directory.

        Raises:
            CreateDirException: If the directory creation operation fails.
        """
        raise NotImplementedError
