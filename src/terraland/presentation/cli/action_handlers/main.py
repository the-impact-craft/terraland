import functools
from typing import Type

from terraland.presentation.cli.action_handlers.base import BaseTerraformActionHandler


class ActionHandlersRegistry(dict):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, *args, **kwargs):
        if self.__initialized:
            return
        super().__init__()
        self.__initialized = True

    def register(self, name: str, handler: Type[BaseTerraformActionHandler]):
        """
        Register a new action handler.
        Args:
            name(str): The name of the action handler.
            handler(subclass of BaseTerraformActionHandler): The action handler class to register
        """
        if not issubclass(handler, BaseTerraformActionHandler):
            raise ValueError("Handler must be an instance of BaseTerraformActionHandler")
        self[name] = handler
        return self


def action_handler(name):
    def wrapper(cls):
        action_handler_registry.register(name, cls)

        @functools.wraps(cls)
        def wrapped(*args, **kwargs):
            return cls(*args, **kwargs)

        return wrapped

    return wrapper


# Singleton registry instance
action_handler_registry = ActionHandlersRegistry()
