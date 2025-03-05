from dataclasses import dataclass
from pathlib import Path


@dataclass
class SearchResult:
    """
    Represents the result of a search operation.

    This class encapsulates the details of a single search result, including
    the matched text, the file where the match was found, and the line number
    within the file. It is typically used to store and organize search results
    for further processing or display.

    Attributes:
        text (str): The text that matched the search pattern.
        file_name (str): The name of the file where the text was found.
        line (int): The line number within the file where the text was found.
    """

    text: str
    file_name: str
    line: int


@dataclass
class SearchResultOutput:
    pattern: str
    output: list[SearchResult]
    total: int


@dataclass
class ListDirOutput:
    """
    Represents the output of a list directory operation.

    This class encapsulates the details of a list directory operation,
    including the list of files and directories within the specified
    directory. It is typically used to store and organize the directory
    listing for further processing or display.
    """

    files: list[Path]
    directories: list[Path]
