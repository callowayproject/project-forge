"""Tests for the `project_forge.task` module."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError
from pytest import param

from project_forge.models.task import Task, execute_task


class TestTask:
    """Tests for the `Task` class."""

    def test_command_as_string_sets_use_shell_true(self):
        """Ensure that `use_shell` is True if `command` is a string."""
        task = Task(command="echo 'Hello, World!'")
        assert task.use_shell is True

    def test_command_as_list_keeps_use_shell_default(self):
        """Ensure that `use_shell` remains the default value when `command` is a list."""
        task = Task(command=["echo", "Hello, World!"])
        assert task.use_shell is False

    def test_env_can_be_set(self):
        """Ensure that `env` can be set and accessed."""
        env_dict = {"VAR1": "value1", "VAR2": "value2"}
        task = Task(command="echo 'Testing'", env=env_dict)
        assert task.env == env_dict

    def test_when_field_is_set_correctly(self):
        """Ensure that `when` is set correctly."""
        condition = "{{ some_condition }}"
        task = Task(command="echo 'Task when condition met'", when=condition)
        assert task.when == condition

    def test_context_variable_name_can_be_set(self):
        """Ensure that `context_variable_name` is set and accessed."""
        task = Task(command="echo 'Test output'", context_variable_name="output_variable")
        assert task.context_variable_name == "output_variable"

    def test_invalid_instance_raises_validation_error(self):
        """Ensure that invalid instances raise a ValidationError."""
        with pytest.raises(ValidationError):
            Task(use_shell="invalid_value")  # Invalid use_shell type

    def test_validate_use_shell_with_string_command(self):
        """Ensure `validate_use_shell` sets `use_shell` correctly for string commands."""
        task = Task(command="ls -la")
        assert task.use_shell is True

    def test_validate_use_shell_with_list_command(self):
        """Ensure `validate_use_shell` keeps `use_shell` default for list commands."""
        task = Task(command=["ls", "-la"])
        assert task.use_shell is False


class TestExecuteTask:
    """Tests for the `execute_task` function."""

    def test_executes_when_condition_is_met(self, tmp_path: Path):
        """When the tasks `when` condition is met, the task is executed."""
        # Assemble
        task = MagicMock(when=None, env=None, use_shell=True, command="echo test", context_variable_name=None)
        context = {"output_dir": tmp_path, "context_variable_name": None}

        with (
            patch("project_forge.models.task.render_bool_expression", return_value=True),
            patch("subprocess.run") as mock_run,
        ):
            # Act
            result_context = execute_task(task, context)

            # Assert
            mock_run.assert_called_once()
            assert result_context == context

    def test_skips_when_condition_is_not_met(self, tmp_path: Path):
        """When the tasks `when` condition is not met, the task is skipped."""
        # Assemble
        task = MagicMock(when=False, env=None, use_shell=True, command="echo test", context_variable_name=None)
        context = {"output_dir": tmp_path}

        with patch("project_forge.models.task.render_bool_expression", return_value=False):
            # Act
            result_context = execute_task(task, context)

            # Assert
            assert result_context == context

    def test_updates_context_with_command_output(self, tmp_path: Path):
        """When a tasks `context_variable_name` is set, the updated context is returned."""
        # Assemble
        task = MagicMock(when=None, env=None, use_shell=True, command="echo test", context_variable_name="output")
        context = {"output_dir": tmp_path}

        with patch(
            "subprocess.run", return_value=subprocess.CompletedProcess(args=[], returncode=0, stdout=b"test\n")
        ):
            # Act
            result_context = execute_task(task, context)

            # Assert
            assert result_context["output"] == "test"

    def test_raises_error_on_subprocess_failure(self, tmp_path: Path):
        """When a command fails, an error is raised."""
        # Assemble
        task = MagicMock(when=None, env=None, use_shell=True, command="echo test", context_variable_name=None)
        context = {"output_dir": tmp_path}

        with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "invalid_command")):
            with pytest.raises(subprocess.CalledProcessError):
                # Act
                execute_task(task, context)

    @pytest.mark.parametrize(
        ["command"],
        [
            param(["echo", "{{ my_variable }}"], id="command-list"),
            param("echo {{ my_variable }}", id="command-string"),
        ],
    )
    def test_renders_context_variables_in_command_list(self, command: list | str, tmp_path: Path):
        """Context variables in the command are rendered before executing."""
        # Assemble
        task = Task(command=command, context_variable_name="result")
        context = {"output_dir": tmp_path, "my_variable": "test"}

        # Act
        result_context = execute_task(task, context)

        # Assert
        assert result_context["result"] == "test"
