from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from project_forge.cli import build
from project_forge.ui.defaults import return_defaults
from project_forge.ui.terminal import ask_question


@pytest.fixture
def runner():
    """The CLI runner."""
    return CliRunner()


@pytest.fixture
def composition_path(tmp_path: Path):
    """The path to a composition file."""
    path = tmp_path / "composition.yaml"
    path.touch(exist_ok=True)
    return path


class TestBuildCommand:
    """
    Tests for the cli.build command.

    Doesn't test the implementation, just the CLI interface.
    """

    @patch("project_forge.commands.build.build_project")
    def test_use_defaults_changes_ui_function(self, mock_build_project, runner: CliRunner, composition_path: Path):
        """The `use-defaults` flag correctly changes the UI function passed to the `build_project` function."""
        result = runner.invoke(build, [str(composition_path), "--use-defaults"])

        if result.exit_code != 0:
            print(result.output)

        assert result.exit_code == 0
        mock_build_project.assert_called_once_with(
            composition_path,
            output_dir=Path.cwd(),
            ui_function=return_defaults,
            initial_context={"output_dir": Path.cwd()},
        )

    @patch("project_forge.commands.build.build_project")
    def test_custom_output_dir_passed_to_build_project(
        self, mock_build_project, runner: CliRunner, composition_path: Path, tmp_path: Path
    ):
        """The `output-dir` option is correctly passed to the `build_project` function."""
        output_dir = tmp_path / "custom-dir"
        output_dir.mkdir(parents=True, exist_ok=True)

        result = runner.invoke(build, [str(composition_path), "--output-dir", str(output_dir)])

        if result.exit_code != 0:
            print(result.output)

        assert result.exit_code == 0
        mock_build_project.assert_called_once_with(
            composition_path,
            output_dir=output_dir,
            ui_function=ask_question,
            initial_context={"output_dir": output_dir},
        )

    @patch("project_forge.commands.build.build_project")
    @patch("project_forge.cli.parse_file")
    def test_data_file_adds_to_initial_context(
        self, mock_parse_file, mock_build_project, runner: CliRunner, composition_path: Path, tmp_path: Path
    ):
        """The parsed results of a data file are added to the initial context."""
        data_file_path = tmp_path / "data.yaml"
        data_file_path.touch(exist_ok=True)
        mock_parse_file.return_value = {"key": "value"}

        result = runner.invoke(build, [str(composition_path), "--data-file", str(data_file_path)])

        if result.exit_code != 0:
            print("OUTPUT:", result.output, result)

        assert result.exit_code == 0

        mock_parse_file.assert_called_once_with(data_file_path)
        mock_build_project.assert_called_once_with(
            composition_path,
            output_dir=Path.cwd(),
            ui_function=ask_question,
            initial_context={"key": "value", "output_dir": Path.cwd()},
        )

    @patch("project_forge.commands.build.build_project")
    def test_data_options_adds_to_initial_context(self, mock_build_project, runner: CliRunner, composition_path: Path):
        """Data options are added to the initial context."""
        result = runner.invoke(build, [str(composition_path), "-d", "key", "value"])

        if result.exit_code != 0:
            print(result.output)

        assert result.exit_code == 0
        mock_build_project.assert_called_once_with(
            composition_path,
            output_dir=Path.cwd(),
            ui_function=ask_question,
            initial_context={"key": "value", "output_dir": Path.cwd()},
        )
