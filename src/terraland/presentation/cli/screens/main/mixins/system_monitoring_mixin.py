import asyncio

from textual import work
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

from terraland.presentation.cli.messages.file_system_change_event import FileSystemChangeEvent
from terraland.settings import SYSTEM_EVENTS_MONITORING_TIMEOUT


class SystemMonitoringMixin:
    required_methods = [
        "refresh_env",
        "update_selected_file_content",
        "remove_tab_for_deleted_file",
    ]

    required_attributes = [
        "work_dir",
        "terraform_core_service",
    ]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        for attribute in cls.required_attributes:
            if not hasattr(cls, attribute):
                raise AttributeError(f"Class {cls.__name__} must have attribute {attribute}")

        for method in cls.required_methods:
            if not callable(getattr(cls, method, None)):
                raise TypeError(f"Class {cls.__name__} must implement method {method}")

    def __init__(self):
        self.updated_events_count = 0
        self.observer = None

    @work()
    async def start_system_events_monitoring(self):
        """
        Asynchronously starts monitoring system events within a specific directory.

        This function utilizes an observer pattern to monitor file system events such
        as creation, modification, deletion, or movement within the specified directory.
        When an event is detected, a FileSystemChangeEvent message is posted to the
        application, which is handled by the on_file_system_change_event method that:
         1. Tracks the number of file system events
         2. Updates the UI when monitored files are modified
         3. Removes tabs when monitored files are deleted

        The monitoring process runs continuously until explicitly stopped or interrupted.
        """

        class EventHandler(FileSystemEventHandler):
            def __init__(self, handler: callable, *args, **kwargs):  # type: ignore
                super().__init__(*args, **kwargs)
                self.handler = handler

            def on_any_event(self, event: FileSystemEvent) -> None:
                self.handler(event)

        event_handler = EventHandler(lambda event: self.post_message(FileSystemChangeEvent(event)))  # type: ignore
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.work_dir), recursive=True)  # type: ignore
        self.observer.start()
        try:
            while True:
                await asyncio.sleep(1)
        finally:
            self.cleanup_observer()

    @work()
    async def start_sync_monitoring(self):
        """
        This method asynchronously starts monitoring for system updates. It checks periodically if any system
        updates have been detected. After processing the updates, it resets the update counter, updates the last
        synchronization date, and refreshes the environment settings. The monitoring loop runs indefinitely unless
        stopped by external control or exceptions. It ensures to log a warning message when the monitoring ceases.

        We run a separate monitoring loop to check for system updates not to trigger full environment refreshes on every
        file system event.
        """
        try:
            while True:
                await asyncio.sleep(SYSTEM_EVENTS_MONITORING_TIMEOUT)
                if self.updated_events_count > 0 and not self.pause_system_monitoring:  # type: ignore
                    self.updated_events_count = 0
                    self.refresh_env()  # type: ignore #  method is in required_methods
        finally:
            self.log.warning("System updates monitoring stopped")  # type: ignore #  method is in required_methods

    def cleanup_observer(self):
        """Stop and cleanup the file system observer."""
        if getattr(self, "observer"):
            if self.observer is None:
                return
            self.observer.stop()
            self.observer.join()

    def on_file_system_change_event(self, event: FileSystemChangeEvent):
        self.updated_events_count += 1
        if event.system_event.event_type == "modified":
            self.update_selected_file_content(event.system_event)  # type: ignore #  method is in required_methods
        elif event.system_event.event_type == "deleted":
            self.remove_tab_for_deleted_file(event.system_event)  # type: ignore #  method is in required_methods
