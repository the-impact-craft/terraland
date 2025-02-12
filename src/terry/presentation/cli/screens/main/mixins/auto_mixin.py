from typing import Type, Any


class AutoMixin:
    """
    A mixin class that automatically injects methods from base classes.

    The AutoMixin class inspects its base classes and automatically attaches 
    methods that start with "on_" from the base classes to the deriving class 
    if such methods do not already exist in the subclass.
    """

    def __init_subclass__(cls: Type['AutoMixin'], **kwargs: Any):
        super().__init_subclass__(**kwargs)

        # Collect all mixin methods that start with `on_`
        for base in cls.__bases__:
            for attr_name in dir(base):
                if attr_name.startswith("on_") and callable(getattr(base, attr_name)):
                    # Attach the method to the subclass if not already present
                    if not hasattr(cls, attr_name):
                        setattr(cls, attr_name, getattr(base, attr_name))