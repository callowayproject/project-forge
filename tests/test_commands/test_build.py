"""Tests for the `project_forge.commands.build` module."""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from project_forge.commands.build import build_project
from project_forge.core.types import BuildResult
from project_forge.ui.defaults import return_defaults
from project_forge.utils import inside_dir


@pytest.fixture(scope="module")
def composition_contents(fixtures_dir: Path) -> str:
    """Create the contents of a composition file."""
    pattern1 = fixtures_dir / "python-package/pattern.toml"
    pattern2 = fixtures_dir / "mkdocs/pattern.toml"
    pattern3 = fixtures_dir / "python-boilerplate/pattern.toml"
    return "\n".join(
        [
            "steps = [",
            f"    {{ pattern_location = '{pattern1}' }},",
            f"    {{ pattern_location = '{pattern2}' }},",
            f"    {{ pattern_location = '{pattern3}' }},",
            '     { command = ["git", "init"] },',
            "]\n",
        ]
    )


class TestBuildProject:
    """Tests for the build_project function."""

    def test_builds_project_with_defaults(self, tmp_path: Path, composition_contents: str):
        """Tests the function with `use_defaults=True`."""
        # Arrange
        composition_file = tmp_path / "composition.toml"
        composition_file.write_text(composition_contents)
        output_dir = tmp_path / "output"
        expected_dir = output_dir / "my-project"
        ui_function = return_defaults

        # Act
        with inside_dir(tmp_path):
            result = build_project(composition_file, output_dir, ui_function)

        # Assert
        assert isinstance(result, BuildResult)
        assert result.root_path == expected_dir
        assert expected_dir.joinpath("README.md").exists()
        assert expected_dir.joinpath("CHANGELOG.md").exists()
        assert expected_dir.joinpath("pyproject.toml").exists()

    def test_missing_composition_file_raises_error(self, tmp_path: Path):
        """If a composition file does not exist, a file not found error should be raised."""
        # Assemble
        output_dir = tmp_path / "output"
        composition_file = tmp_path / "nonexistent.yaml"
        ui_function = MagicMock()

        # Act, Assert
        with pytest.raises(FileNotFoundError):
            build_project(composition_file, output_dir, ui_function)

    def test_initial_context_is_used(self, tmp_path: Path, composition_contents: str):
        """Tests that the `initial_context` parameter is merged into the final result."""
        composition_file = tmp_path / "composition.toml"
        composition_file.write_text(composition_contents)
        output_dir = tmp_path / "output"
        expected_dir = output_dir / "test-project"
        ui_function = return_defaults
        initial_context = {"project_name": "Test Project"}

        with inside_dir(tmp_path):
            result = build_project(composition_file, output_dir, ui_function, initial_context=initial_context)

        assert result.context["project_name"] == initial_context["project_name"]
        assert result.root_path == expected_dir
        assert expected_dir.exists()

    def test_initial_context_is_used_with_defaults(self, tmp_path: Path, composition_contents: str):
        """Tests that the `initial_context` parameter is merged into the defaults."""
        # Assemble
        composition_file = tmp_path / "composition.toml"
        composition_file.write_text(composition_contents)
        output_dir = tmp_path / "output"
        expected_dir = output_dir / "test-project"
        ui_function = return_defaults
        initial_context = {"project_name": "Test Project"}

        # Act
        with inside_dir(tmp_path):
            result = build_project(composition_file, output_dir, ui_function, initial_context=initial_context)

        # Assert
        assert result.context["project_name"] == initial_context["project_name"]
        assert result.context["repo_name"] == "test-project"
        assert result.root_path == expected_dir
        assert expected_dir.exists()
