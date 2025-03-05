from dataclasses import dataclass

from textual.message import Message
from watchdog.events import FileSystemEvent


@dataclass
class FileSystemChangeEvent(Message):
    system_event: FileSystemEvent
