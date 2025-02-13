import asyncio

from textual import work
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

from terry.settings import SYSTEM_EVENTS_MONITORING_TIMEOUT


class SystemMonitoringMixin:
    required_methods = ["refresh_env", "update_selected_file_content"]

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
            if not hasattr(cls, method) or not callable(getattr(cls, method)):
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
        When an event is detected, the following handlers are invoked in order:
        1. increment_updated_events: Tracks the number of file system events
        2. update_selected_file_content: Updates the UI when monitored files change

        The monitoring process runs continuously until explicitly stopped or interrupted.
        """

        class EventHandler(FileSystemEventHandler):
            def __init__(self, handlers: list[callable], *args, **kwargs):  # type: ignore
                super().__init__(*args, **kwargs)
                self.handlers = handlers

            def on_any_event(self, event: FileSystemEvent) -> None:
                for handler in self.handlers:
                    handler(event)

        event_handler = EventHandler(
            [
                self.increment_updated_events,
                self.update_selected_file_content,  # type: ignore #  method is in required_methods
            ]
        )
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
                if self.updated_events_count > 0:
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

    def increment_updated_events(self, _: FileSystemEvent):
        """
        Increments the count of updated events for internal tracking purposes. This
        method modifies the internal `updated_events_count` attribute by adding one
        each time it is invoked.

        Arguments:
            _: The event object whose update triggers the increment.
        """
        self.updated_events_count += 1
