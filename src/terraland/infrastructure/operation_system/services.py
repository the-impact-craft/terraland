import os
import platform
from typing import List

from terraland.domain.operation_system.entities import OperationSystem, Variable, EnvVariableFilter
from terraland.domain.operation_system.services import BaseOperationSystemService
from terraland.infrastructure.operation_system.exceptions import EnvVarOperationSystemException


class OperationSystemService(BaseOperationSystemService):
    def get_operation_system(self) -> OperationSystem:
        """
        Gets the operating system information.

        This function retrieves the name and version of the operating system
        using the `platform` module and returns it as an `OperationSystem` object.

        Returns:
            OperationSystem: Contains the `name` of the operating system and its
            `version` as captured by the `platform` module.
        """

        return OperationSystem(
            name=platform.system(),
            version=platform.release(),
        )

    def list_environment_variables(self, vars_filter: EnvVariableFilter | None = None) -> List[Variable]:
        """
        Lists the environment variables filtered by the provided criteria if applicable.

        This method retrieves all environment variables from the current system. If a
        filter is provided, only variables matching the specified filter criteria are
        included in the result. Each environment variable is represented as an instance
        of `Variable`, containing its name and value.

        Arguments:
            vars_filter (EnvVariableFilter | None): A filter object that specifies the
                criteria to match environment variable names. If None, all environment
                variables are returned.

        Returns:
            List[Variable]: A list of environment variables. Each variable includes
                its name and value.
        """
        env_vars = list(os.environ.items())
        if not vars_filter:
            return [Variable(name=name, value=value) for name, value in env_vars]

        return [
            Variable(name=name, value=value)
            for name, value in env_vars
            if self._env_var_name_matches_filter(name, vars_filter)
        ]

    def set_environment_variable(self, key: str, value: str):
        """
        Sets an environment variable in the operating system.

        This method updates the current process's environment to include or modify
        the specified key-value pair.

        Arguments:
            key (str): The name of the environment variable to set. Must be a
                non-empty string.
            value (str): The value to associate with the environment variable. Must
                be a string.

        Raises:
            EnvVarOperationSystemException: If the key or value is not a string or
                the key is an empty string.
        """
        if not isinstance(key, str) or not isinstance(value, str):
            raise EnvVarOperationSystemException("Key and value must be strings")
        if not key:
            raise EnvVarOperationSystemException("Key cannot be empty")
        os.environ[key] = value

    def unset_environment_variable(self, key: str):
        """
        Removes an environment variable from the system's environment.

        The method attempts to remove an environment variable specified by the
        `key`. If the `key` is invalid (empty or not a string), an exception
        specific to environment variable operations is raised. The method safely
        handles cases where the `key` may not exist in the environment.

        Arguments:
            key: The name of the environment variable to unset. It should be a
                non-empty string.

        Raises:
            EnvVarOperationSystemException: If the `key` is empty or not a string.
        """
        if not key:
            raise EnvVarOperationSystemException("Key cannot be empty")
        if not isinstance(key, str):
            raise EnvVarOperationSystemException("Key must be a string")

        os.environ.pop(key, None)

    def get_environment_variable(self, key: str) -> Variable:
        """
        Retrieves the value of an environment variable by its key.

        This function retrieves the value of a given environment variable from the
        system's environment. It validates the input key to ensure it is a non-empty
        string and raises an exception if these conditions are not met. The function
        then returns an Variable object containing the key and its corresponding
        value.

        Arguments:
            key: The name of the environment variable to retrieve. Must be a non-empty
                string.

        Raises:
            EnvVarOperationSystemException: If the key is empty or not of type string.

        Returns:
            Variable: An object representing the environment variable, including
            its name and value where the value is fetched from the system's
            environment.
        """
        if not key:
            raise EnvVarOperationSystemException("Key cannot be empty")
        if not isinstance(key, str):
            raise EnvVarOperationSystemException("Key must be a string")

        return Variable(name=key, value=os.environ.get(key))

    @staticmethod
    def _env_var_name_matches_filter(name: str, vars_filter: EnvVariableFilter | None = None) -> bool:
        """
        Checks if an environment variable name matches the given filter criteria.

        The method evaluates if the environment variable `name` meets all specified
        filtering criteria from the `vars_filter`. The filtering conditions include
        checking for prefix, suffix, and a substring within the variable name. If no
        filter criteria are provided, it will default to returning True.

        Arguments:
            name (str): The name of the environment variable to check.
            vars_filter (EnvVariableFilter | None): The filter criteria to apply, or
                None if no filtering is required.

        Returns:
            bool: True if the variable name matches the filter criteria, False
            otherwise.
        """

        if vars_filter is None:
            return True

        if vars_filter.prefix:
            if isinstance(vars_filter.prefix, str):
                if not name.startswith(vars_filter.prefix):
                    return False
            if isinstance(vars_filter.prefix, list):
                if not any(name.startswith(prefix) for prefix in vars_filter.prefix):
                    return False

        if vars_filter.suffix and not name.endswith(vars_filter.suffix):
            return False

        if vars_filter.contains and vars_filter.contains not in name:
            return False

        return True
