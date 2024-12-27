from pathlib import Path
from unittest.mock import patch

import pytest

from project_forge.core.exceptions import (
    RepoAuthError,
    RepoNotFoundError,
)
from project_forge.models.composition import Composition, read_composition_file
from project_forge.models.location import Location
from project_forge.models.overlay import _validate_pattern_location  # noqa: PLC2701
from project_forge.models.task import Task
from tests.mocks import MockValidationInfo


class TestValidateTemplateLocation:
    """Tests for the _validate_pattern_location function."""

    def test_string_location_is_converted_to_location(self, tmp_path: Path):
        """A string value is converted to a Location object."""
        expected_path = tmp_path.joinpath("template")
        expected_path.touch()
        expected_location = Location(path=str(expected_path))
        response = _validate_pattern_location(expected_location.path, MockValidationInfo())
        assert response == expected_location

    def test_uses_context_to_resolve_relative_path(self, tmp_path: Path):
        """The presence of `pattern_path` in the context is used to resolve relative paths."""
        expected_path = tmp_path.joinpath("template")
        expected_path.touch()
        composition_path = tmp_path.joinpath("composition")
        composition_path.touch()

        location = Location(path="template")
        mock_info = MockValidationInfo(context={"composition_path": composition_path})
        actual = _validate_pattern_location(location, mock_info)
        assert actual == location

    def test_location_not_file_raises_value_error(self, tmp_path: Path):
        """A Location that points to a directory raises a ValueError."""
        location = Location(path=str(tmp_path))
        with pytest.raises(ValueError):
            _validate_pattern_location(location, MockValidationInfo())

    def test_missing_repo_raises_value_error(self):
        """A Location with a missing url attribute raises a ValueError."""

        def mock_resolve(*args):
            raise RepoNotFoundError()

        with patch("project_forge.models.location.Location", spec=Location, resolve=mock_resolve) as MockLocation:
            # Use a mocked Location object whose `resolve` method always raises a RepoNotFound error
            with pytest.raises(ValueError):
                _validate_pattern_location(MockLocation(), MockValidationInfo())

    def test_unauthenticated_repo_raises_value_error(self):
        """A Location with an unauthenticated url attribute raises a ValueError."""

        def mock_resolve(*args):
            raise RepoAuthError()

        with patch("project_forge.models.location.Location", spec=Location, resolve=mock_resolve) as MockLocation:
            # Use a mocked Location object whose `resolve` method always raises a RepoAuthError
            with pytest.raises(ValueError):
                _validate_pattern_location(MockLocation(), MockValidationInfo())

    def test_missing_path_raises_value_error(self):
        """If the location does not exist, a ValueError is raised."""
        location = Location(path="/invalid/location")
        with pytest.raises(ValueError):
            _validate_pattern_location(location, MockValidationInfo())


def test_create_composition_from_str_location(tmp_path: Path):
    """You can create a Composition from a string location."""
    template = tmp_path.joinpath("template")
    template.touch()
    comp = Composition.from_location(str(template))
    assert comp.steps[0].pattern_location.path == str(template)


def test_create_composition_from_location(tmp_path: Path):
    """You can create a Composition from a string location."""
    template = tmp_path.joinpath("template")
    template.touch()
    location = Location(path=str(template))
    comp = Composition.from_location(location)
    assert comp.steps[0].pattern_location.path == str(template)


class TestReadCompositionFile:
    """Test for the `read_composition_file` function."""

    def test_reads_a_composition_file(self, fixtures_dir: Path):
        """The composition and its patterns are correctly read from a file."""
        composition = read_composition_file(fixtures_dir / "composition1.toml")
        assert len(composition.steps) == 4
        pattern1 = composition.steps[0].pattern
        pattern2 = composition.steps[1].pattern
        pattern3 = composition.steps[2].pattern
        command = composition.steps[3].command

        assert pattern1 is not None
        assert len(pattern1.questions) == 6
        assert pattern1.template_location.resolve() == fixtures_dir / "python-package" / "{{ repo_name }}"

        assert pattern2 is not None
        assert len(pattern2.questions) == 4
        assert pattern2.template_location.resolve() == fixtures_dir / "mkdocs" / "{{ repo_name }}"

        assert pattern3 is not None
        assert len(pattern3.questions) == 8
        assert pattern3.template_location.resolve() == fixtures_dir / "python-boilerplate" / "{{ repo_name }}"

        assert isinstance(composition.steps[3], Task)
        assert command == ["git", "init"]

    def test_reads_and_converts_a_pattern_file(self, fixtures_dir: Path):
        """A pattern file is read and converted into a composition with one overlay."""
        composition = read_composition_file(fixtures_dir / "mkdocs" / "pattern.toml")
        assert len(composition.steps) == 1
        pattern = composition.steps[0].pattern
        assert pattern is not None
        assert len(pattern.questions) == 4
        assert pattern.template_location.resolve() == fixtures_dir / "mkdocs" / "{{ repo_name }}"


# TODO[#7]: Write composition test scenario patterns with optional questions
# TODO[#8]: Write composition test scenario patterns with optional questions that are answered in a previous pattern
# TODO[#9]: Write composition test scenario patterns with files/directories named with mapped keys. They should properly get mapped to the combined template structure
# TODO[#10]: Write composition test scenario patterns with mixed file types
