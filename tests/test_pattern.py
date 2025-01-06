"""Tests for project_forge.configurations.pattern."""

from pathlib import Path
from unittest.mock import patch

import pytest
from pytest import param

from project_forge.core.exceptions import PathNotFoundError, RepoAuthError, RepoNotFoundError
from project_forge.models.location import Location
from project_forge.models.pattern import (
    Choice,
    Pattern,
    Question,
    _validate_template_location,
    find_template_root,
)
from project_forge.rendering.templates import ProcessMode
from tests.mocks import MockValidationInfo


class TestValidateTemplateLocation:
    """Tests for the _validate_template_location function."""

    def test_string_location_is_converted_to_location(self, tmp_path: Path):
        """A string value is converted to a Location object."""
        expected_location = Location(path=str(tmp_path))
        response = _validate_template_location(expected_location.path, MockValidationInfo())
        assert response == expected_location

    def test_uses_context_to_resolve_relative_path(self, tmp_path: Path):
        """The presence of `pattern_path` in the context is used to resolve relative paths."""
        template_dir = tmp_path.joinpath("template")
        template_dir.mkdir(exist_ok=True, parents=True)
        location = Location(path="template")
        mock_info = MockValidationInfo(context={"pattern_path": tmp_path})
        with patch("project_forge.models.pattern.find_template_root", return_value=template_dir):
            actual = _validate_template_location(location, mock_info)
            assert actual == location

    def test_missing_repo_raises_value_error(self):
        """A Location with a missing url attribute raises a ValueError."""

        def mock_resolve(*args):
            raise RepoNotFoundError()

        with patch("project_forge.models.pattern.Location", spec=Location, resolve=mock_resolve) as MockLocation:
            # Use a mocked Location object whose `resolve` method always raises a RepoNotFound error
            with pytest.raises(ValueError):
                _validate_template_location(MockLocation(), MockValidationInfo())

    def test_unauthenticated_repo_raises_value_error(self):
        """A Location with an unauthenticated url attribute raises a ValueError."""

        def mock_resolve(*args):
            raise RepoAuthError()

        with patch("project_forge.models.pattern.Location", spec=Location, resolve=mock_resolve) as MockLocation:
            # Use a mocked Location object whose `resolve` method always raises a RepoAuthError
            with pytest.raises(ValueError):
                _validate_template_location(MockLocation(), MockValidationInfo())

    def test_missing_path_raises_value_error(self):
        """If the location does not exist, a ValueError is raised."""
        location = Location(path="/invalid/location")
        with pytest.raises(ValueError):
            _validate_template_location(location, MockValidationInfo())


class TestFindTemplateRoot:
    """Tests for the find_template_root function."""

    def test_finds_directory_with_prefix_in_root_path(self, tmp_path: Path):
        """If there is a directory starting with the prefix, it is found."""
        # Assemble
        root_path = tmp_path
        template_dir = root_path.joinpath("{{ template }}")
        template_dir.mkdir(exist_ok=True, parents=True)
        prefix = "{{"

        # Act
        try:
            template_root = find_template_root(root_path, prefix)
            assert template_root == template_dir
        except PathNotFoundError as e:
            pytest.fail(str(e))

    def test_no_directory_with_prefix_in_root_path_raises_error(self, tmp_path: Path):
        """If there is no directory starting with the prefix, an error is raised."""
        root_path = tmp_path
        prefix = "{{"

        with pytest.raises(PathNotFoundError, match="Could not find a directory in.*starting with.*"):
            find_template_root(root_path, prefix)

    def test_missing_root_directory_raises_error(self):
        """A missing root directory raises an error."""
        root_path = Path("/idontexist/")
        prefix = "{{"
        # Test expected behavior
        with pytest.raises(PathNotFoundError, match="The root path.*does not exist."):
            find_template_root(root_path, prefix)


class TestPattern:
    """Tests for the Pattern class."""

    def test_str_template_location_is_converted_to_location(self, tmp_path: Path):
        """A string value is converted to a Location object for the template_location field."""
        template_path = tmp_path.joinpath("{{ template }}")
        template_path.mkdir(exist_ok=True, parents=True)
        data = {
            "questions": [],
            "template_location": str(tmp_path),
        }
        pattern = Pattern(**data)
        assert pattern.template_location == Location(path=str(tmp_path))


class TestChoice:
    """Tests for the Choice class."""

    def test_dicts_converted_to_choices(self):
        """Dictionaries with a proper label and value are converted to Choice objects."""
        question_data = {
            "name": "test",
            "choices": [
                {"label": "choice1", "value": 1},
                {"label": "choice2", "value": 2},
            ],
        }
        question = Question(**question_data)
        assert all(isinstance(choice, Choice) for choice in question.choices)

    @pytest.mark.parametrize(
        ["values", "labels"],
        [
            param([1, 2, 3], ["_1", "_2", "_3"], id="ints"),
            param([True, False], ["True", "False"], id="bools"),
            param([1.0, 2.0, 3.0], ["_1_0", "_2_0", "_3_0"], id="floats"),
            param(["a", "b", "c"], ["a", "b", "c"], id="strings"),
            param([None, None, None], ["None", "None", "None"], id="none"),
        ],
    )
    def test_scalar_choices_converted_to_choice(self, values: list, labels: list):
        """A scalar choice is converted to a Choice object."""
        question_data = {
            "name": "test",
            "choices": values,
        }
        question = Question(**question_data)
        assert all(isinstance(choice, Choice) for choice in question.choices)
        for index, choice in enumerate(question.choices):
            assert choice.value == values[index]
            assert choice.label == labels[index]

    @pytest.mark.parametrize(
        ["values", "labels"],
        [
            param([1, 2, 3], ["_1", "_2", "_3"], id="ints"),
            param([True, False], ["True", "False"], id="bools"),
            param([1.0, 2.0, 3.0], ["_1_0", "_2_0", "_3_0"], id="floats"),
            param(["a", "b", "c"], ["a", "b", "c"], id="strings"),
            param([None, None, None], ["None", "None", "None"], id="none"),
        ],
    )
    def test_missing_label_is_generated(self, values: list, labels: list):
        """If a choice is missing its label attribute, it is generated."""
        question_data = {
            "name": "test",
            "choices": [{"value": value} for value in values],
        }
        question = Question(**question_data)

        assert all(isinstance(choice, Choice) for choice in question.choices)
        for index, choice in enumerate(question.choices):
            assert choice.value == values[index]
            assert choice.label == labels[index]

    @pytest.mark.parametrize(
        ["values", "labels"],
        [
            param([1, 2, 3], ["_1", "_2", "_3"], id="ints"),
            param([True, False], ["True", "False"], id="bools"),
            param([1.0, 2.0, 3.0], ["_1_0", "_2_0", "_3_0"], id="floats"),
            param(["a", "b", "c"], ["a", "b", "c"], id="strings"),
            param([None, None, None], ["None", "None", "None"], id="none"),
        ],
    )
    def test_empty_label_is_generated(self, values: list, labels: list):
        """If a choice has an empty label attribute, it is generated."""
        question_data = {
            "name": "test",
            "choices": [{"value": value, "label": ""} for value in values],
        }
        question = Question(**question_data)

        assert all(isinstance(choice, Choice) for choice in question.choices)
        for index, choice in enumerate(question.choices):
            assert choice.value == values[index]
            assert choice.label == labels[index]


class TestGetProcessMode:
    """Tests for the get_process_mode method in the Pattern class."""

    @pytest.fixture
    def pattern(self, fixtures_dir: Path):
        """Fixture for creating a Pattern instance."""
        return Pattern(
            questions=[],
            template_location=str(fixtures_dir.joinpath("python-package", "{{ repo_name }}")),
            extra_context={},
            template_engine="default",
            template_engine_ops={},
            skip=[],
            copy_only=[],
            migrations=[],
        )

    def test_default_mode_is_render_write(self, pattern):
        """Test that default process mode is render and write."""
        path = Path("some/path")
        mode = pattern.get_process_mode(path)
        assert mode == (ProcessMode.render | ProcessMode.write)

    def test_process_mode_skip_only(self, pattern):
        """Test that a path matching skip excludes the write mode."""
        pattern.skip = ["some/*"]
        path = Path("some/path")
        mode = pattern.get_process_mode(path)
        assert mode == ProcessMode.render

    def test_process_mode_copy_only(self, pattern):
        """Test that a path matching copy_only excludes the render mode."""
        pattern.copy_only = ["some/*"]
        path = Path("some/path")
        mode = pattern.get_process_mode(path)
        assert mode == ProcessMode.write

    def test_process_mode_skip_and_copy_only(self, pattern):
        """Test that a path matching both skip and copy_only excludes both modes."""
        pattern.skip = ["some/*"]
        pattern.copy_only = ["some/*"]
        path = Path("some/path")
        mode = pattern.get_process_mode(path)
        assert mode == ProcessMode.ignore

    def test_process_mode_non_matching_path(self, pattern):
        """Test that a non-matching path keeps default modes."""
        pattern.skip = ["other/*"]
        pattern.copy_only = ["another/*"]
        path = Path("some/path")
        mode = pattern.get_process_mode(path)
        assert mode == (ProcessMode.render | ProcessMode.write)
