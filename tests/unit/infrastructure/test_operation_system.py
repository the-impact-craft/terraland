import os

import pytest

from terraland.domain.operation_system.entities import OperationSystem, EnvVariableFilter, Variable
from terraland.infrastructure.operation_system.exceptions import EnvVarOperationSystemException


class TestOperationSystemService:
    def test_get_operation_system_returns_instance_of_operation_system(self, operation_system_service):
        """Test if `get_operation_system` returns an instance of `OperationSystem`."""
        result = operation_system_service.get_operation_system()
        assert isinstance(result, OperationSystem)

    def test_get_operation_system_returns_valid_name(self, operation_system_service):
        """Test if `get_operation_system` returns a valid `name`."""
        result = operation_system_service.get_operation_system()
        assert isinstance(result.name, str)
        assert result.name != ""

    def test_get_operation_system_returns_valid_version(self, operation_system_service):
        """Test if `get_operation_system` returns a valid `version`."""
        result = operation_system_service.get_operation_system()
        assert isinstance(result.version, str)
        assert result.version != ""

    def test_list_environment_variables_returns_all(self, operation_system_service, mock_environment_variables):
        """Test if `list_environment_variables` returns all environment variables when no filter is provided."""
        result = operation_system_service.list_environment_variables()
        assert isinstance(result, list)
        assert len(result) == len(mock_environment_variables)
        for env_var in result:
            assert isinstance(env_var, Variable)
            assert env_var.name in mock_environment_variables
            assert env_var.value == mock_environment_variables[env_var.name]

    def test_list_environment_variables_with_filter(self, operation_system_service, mock_environment_variables):
        """Test if `list_environment_variables` returns filtered environment variables."""
        vars_filter = EnvVariableFilter(prefix="FILTER")
        result = operation_system_service.list_environment_variables(vars_filter=vars_filter)
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].name == "FILTER_VAR"
        assert result[0].value == mock_environment_variables["FILTER_VAR"]

    def test_list_environment_variables_with_list_prefix_filter(
        self, operation_system_service, mock_environment_variables
    ):
        """Test if `list_environment_variables` returns filtered by list_prefix environment variables."""
        vars_filter = EnvVariableFilter(prefix=["FILTER", "ANOTHER"])
        result = operation_system_service.list_environment_variables(vars_filter=vars_filter)
        assert isinstance(result, list)
        assert len(result) == 2
        # Verify specific variables

        assert any(var.name == "FILTER_VAR" and var.value == mock_environment_variables["FILTER_VAR"] for var in result)

        assert any(
            var.name == "ANOTHER_VAR" and var.value == mock_environment_variables["ANOTHER_VAR"] for var in result
        )

    def test_list_environment_variables_with_empty_prefix_list(
        self, operation_system_service, mock_environment_variables
    ):
        vars_filter = EnvVariableFilter(prefix=[])

        result = operation_system_service.list_environment_variables(vars_filter=vars_filter)

        assert isinstance(result, list)
        assert len(result) == len(mock_environment_variables)

    def test_list_environment_variables_with_mixed_prefix_types(
        self, operation_system_service, mock_environment_variables
    ):
        vars_filter = EnvVariableFilter(prefix=["FILTER", b"ANOTHER"])  # type: ignore

        with pytest.raises(TypeError):
            operation_system_service.list_environment_variables(vars_filter=vars_filter)

    def test_list_environment_variables_with_empty_filter(self, operation_system_service, mock_environment_variables):
        """Test if `list_environment_variables` returns no variables when filter matches none."""
        vars_filter = EnvVariableFilter(prefix="DOES_NOT_EXIST")
        result = operation_system_service.list_environment_variables(vars_filter=vars_filter)
        assert isinstance(result, list)
        assert len(result) == 0

    def test_set_environment_variable_sets_value(self, operation_system_service):
        key = "TEST_KEY"
        value = "TEST_VALUE"

        operation_system_service.set_environment_variable(key, value)

        assert os.environ[key] == value

    def test_set_environment_variable_with_empty_value(self, operation_system_service):
        key = "TEST_KEY"
        value = ""

        operation_system_service.set_environment_variable(key, value)

        assert os.environ[key] == value

    def test_set_environment_variable_overwrites_existing_value(self, operation_system_service):
        key = "TEST_KEY"
        initial_value = "INITIAL_VALUE"
        new_value = "NEW_VALUE"

        os.environ[key] = initial_value
        operation_system_service.set_environment_variable(key, new_value)

        assert os.environ[key] == new_value

    def test_set_environment_variable_with_invalid_key(self, operation_system_service):
        key = None
        value = "TEST_VALUE"

        with pytest.raises(EnvVarOperationSystemException):
            operation_system_service.set_environment_variable(key, value)

    def test_set_environment_variable_with_empty_key(self, operation_system_service):
        key = ""
        value = "TEST_VALUE"

        with pytest.raises(EnvVarOperationSystemException):
            operation_system_service.set_environment_variable(key, value)

    def test_set_environment_variable_with_non_str_value(self, operation_system_service):
        key = "test"
        value = 123

        with pytest.raises(EnvVarOperationSystemException):
            operation_system_service.set_environment_variable(key, value)

    def test_set_environment_variable_with_special_characters_in_key(self, operation_system_service):
        key = "TEST@KEY!"
        value = "TEST_VALUE"

        operation_system_service.set_environment_variable(key, value)

        assert os.environ[key] == value

    def test_set_environment_variable_with_large_value(self, operation_system_service):
        key = "TEST_KEY"
        value = "A" * 10_000

        operation_system_service.set_environment_variable(key, value)

        assert os.environ[key] == value

    def test_unset_environment_variable_removes_existing_var(self, operation_system_service):
        os.environ["TEST_VAR"] = "value"

        operation_system_service.unset_environment_variable("TEST_VAR")

        assert "TEST_VAR" not in os.environ

    def test_unset_environment_variable_nonexistent_var(self, operation_system_service):
        result = operation_system_service.unset_environment_variable("NON_EXISTENT_VAR")

        assert result is None  # Since the function uses os.environ.pop(key, None)

    def test_unset_environment_variable_with_empty_key(self, operation_system_service):
        with pytest.raises(EnvVarOperationSystemException):
            operation_system_service.unset_environment_variable("")

    def test_unset_environment_variable_with_special_characters_in_key(self, operation_system_service):
        os.environ["TEST@VAR$"] = "value"

        operation_system_service.unset_environment_variable("TEST@VAR$")

        assert "TEST@VAR$" not in os.environ

    def test_unset_environment_variable_with_invalid_type_key(self, operation_system_service):
        with pytest.raises(EnvVarOperationSystemException):
            operation_system_service.unset_environment_variable(123)  # Invalid type for key

    def test_get_environment_variable_returns_correct_value(self, monkeypatch, operation_system_service):
        monkeypatch.setenv("TEST_VAR", "test_value")

        result = operation_system_service.get_environment_variable("TEST_VAR")
        assert result.name == "TEST_VAR"
        assert result.value == "test_value"

    def test_get_environment_variable_returns_none_for_nonexistent_key(self, operation_system_service):
        result = operation_system_service.get_environment_variable("NONEXISTENT_VAR")
        assert result.name == "NONEXISTENT_VAR"
        assert result.value is None

    def test_get_environment_variable_with_empty_key_raises_exception(self, operation_system_service):
        with pytest.raises(EnvVarOperationSystemException):
            operation_system_service.get_environment_variable("")

    def test_get_environment_variable_with_invalid_type_key_raises_exception(self, operation_system_service):
        with pytest.raises(EnvVarOperationSystemException):
            operation_system_service.get_environment_variable(123)  # Invalid type

    def test_get_environment_variable_with_special_characters_in_key(self, monkeypatch, operation_system_service):
        monkeypatch.setenv("SPECIAL_KEY!@#$", "special_value")

        result = operation_system_service.get_environment_variable("SPECIAL_KEY!@#$")
        assert result.name == "SPECIAL_KEY!@#$"
        assert result.value == "special_value"

    def test_env_var_name_matches_filter_with_prefix(self, operation_system_service):
        vars_filter = EnvVariableFilter(prefix="TEST_")
        assert operation_system_service._env_var_name_matches_filter("TEST_VAR", vars_filter)
        assert not operation_system_service._env_var_name_matches_filter("VAR_TEST", vars_filter)

    def test_env_var_name_matches_filter_with_suffix(self, operation_system_service):
        vars_filter = EnvVariableFilter(suffix="_SUFFIX")
        assert operation_system_service._env_var_name_matches_filter("VAR_SUFFIX", vars_filter)
        assert not operation_system_service._env_var_name_matches_filter("SUFFIX_VAR", vars_filter)

    def test_env_var_name_matches_filter_with_contains(self, operation_system_service):
        vars_filter = EnvVariableFilter(contains="MID")
        assert operation_system_service._env_var_name_matches_filter("VAR_MID_VAR", vars_filter)
        assert not operation_system_service._env_var_name_matches_filter("VAR_VAR", vars_filter)

    def test_env_var_name_matches_filter_with_no_filter(self, operation_system_service):
        vars_filter = EnvVariableFilter()
        assert operation_system_service._env_var_name_matches_filter("ANY_VAR", vars_filter)

    def test_env_var_name_matches_filter_with_combined_filters(self, operation_system_service):
        vars_filter = EnvVariableFilter(prefix="TEST_", suffix="_SUFFIX", contains="MID")
        assert operation_system_service._env_var_name_matches_filter("TEST_MID_SUFFIX", vars_filter)
        assert not operation_system_service._env_var_name_matches_filter("TEST_SUFFIX_MID", vars_filter)
        assert not operation_system_service._env_var_name_matches_filter("MID_TEST_SUFFIX", vars_filter)

    def test_env_var_name_matches_filter_with_none_filter(self, operation_system_service):
        assert operation_system_service._env_var_name_matches_filter("ANY_VAR", None)

    def test_env_var_name_matches_filter_with_empty_filter_values(self, operation_system_service):
        vars_filter = EnvVariableFilter(prefix="", suffix="", contains="")
        assert operation_system_service._env_var_name_matches_filter("ANY_VAR", vars_filter)

    def test_env_var_name_matches_filter_with_special_chars(self, operation_system_service):
        vars_filter = EnvVariableFilter(prefix="@#$")
        assert operation_system_service._env_var_name_matches_filter("@#$VAR", vars_filter)
        assert not operation_system_service._env_var_name_matches_filter("VAR", vars_filter)
