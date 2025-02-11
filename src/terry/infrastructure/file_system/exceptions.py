from terry.domain.file_system.exceptions import BaseFileSystemException


class FileSystemGrepException(BaseFileSystemException):
    """
    Custom exception for errors occurring during a file system search operation.

    This exception is used to indicate and encapsulate errors specific
    to the process of searching and grepping through file system contents.
    It provides additional context about the nature of the error.
    """


class ReadFileException(BaseFileSystemException):
    """
    Custom exception for errors occurring during a file system read operation.

    This exception is used to indicate and encapsulate errors specific
    to the process of reading file contents.
    It provides additional context about the nature of the error.
    """


class ListDirException(BaseFileSystemException):
    """
    Custom exception for errors occurring during a file system list directory operation.

    This exception is used to indicate and encapsulate errors specific
    to the process of listing directory contents.
    It provides additional context about the nature of the error.
    """
