import abc
from typing import List

from terraland.domain.operation_system.entities import OperationSystem, Variable, EnvVariableFilter


class BaseOperationSystemService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_operation_system(self) -> OperationSystem:
        """
        Retrieve the details of an operation system by its unique identifier.

        This method is designed to provide a way to retrieve a specific operation
        system instance, identified by its unique ID, from a data source. The
        implementation details must be provided in subclasses since this is an
        abstract method and does not contain implementation.

        Returns:
            An instance of `OperationSystem`
        """
        raise NotImplementedError

    @abc.abstractmethod
    def list_environment_variables(self, vars_filter: EnvVariableFilter | None = None) -> List[Variable]:
        """
        Lists the environment variables filtered based on the provided criteria.

        This method retrieves the environment variables that meet the conditions
        specified by the given filter. It is required to override this method in
        subclasses to provide specific functionality for processing and returning
        the filtered environment variables.

        Arguments:
            vars_filter: An instance of `EnvVariableFilter` that specifies the criteria
            for filtering the environment variables.
        Returns:
            A list of `Variable` instances that match the filter criteria
            provided.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_environment_variable(self, key: str, value: str):
        """
        Sets an environment variable with a specific key and value.

        This abstract method should be implemented by subclasses to define how
        an environment variable is set. The method takes a key and a value as
        arguments, which represent the name and the corresponding content of
        the environment variable, respectively.

        Arguments:
            key: The name of the environment variable to set.
            value: The content of the environment variable.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def unset_environment_variable(self, key: str):
        """
        Unsets an environment variable with a specific key.

        This method is an abstract method that must be implemented by subclasses
        to define the behavior of unsetting an environment variable. The key
        parameter represents the name of the environment variable that needs to
        be removed.

        Arguments:
            key: The name of the environment variable to unset.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_environment_variable(self, key: str) -> Variable:
        """
        Abstract method to retrieve an environment variable based on the provided key.

        This method should be implemented by subclasses to fetch the respective
        environment variable value. The implementation can vary depending on the
        specific source and format used for environment variables.

        Arguments:
            key: The unique identifier or name of the environment variable to retrieve.

        Returns:
            Variable: An instance of Variable containing the environment variable
            value associated with the provided key.
        """
        raise NotImplementedError
