from abc import ABC, abstractmethod


class BaseTerraformActionHandler(ABC):
    def __init__(self, app):
        self.app = app

    @abstractmethod
    def handle(self, action) -> None:
        """
        Represents an abstract method for handling a specific action. This method is
        designed to be overridden by subclasses to provide specific behavior for the
        given action.

        Args:
            action: The action to be handled. The handling logic must be
                implemented in the subclass.
        :raises NotImplementedError: If the method is called without being
            implemented in a subclass.
        """
        raise NotImplementedError
