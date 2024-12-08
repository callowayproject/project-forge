"""Tests for project_forge.core.io."""

import json
import yaml
from pathlib import Path
from unittest import mock

import pytest
from project_forge.core import io


class TestParseYaml:
    """Tests for project_forge.core.io.parse_yaml."""

    def test_parses_yaml_string(self):
        """A proper YAML string should be parsed."""
        data = {"name": "John", "age": 30, "city": "New York"}
        yaml_str = yaml.dump(data)

        result = io.parse_yaml(yaml_str)
        assert result == data

    def test_invalid_yaml_string_raises_error(self):
        """An invalid YAML string should raise an error."""
        with pytest.raises(yaml.YAMLError):
            io.parse_yaml("unbalanced brackets: ][")

    def test_non_string_input_raises_error(self):
        """A non-string input should raise an error."""
        with pytest.raises(AttributeError):
            io.parse_yaml(None)


class TestParseJson:
    """Tests for project_forge.core.io.parse_json."""

    def test_parses_json_string(self):
        """A proper JSON string should be parsed."""
        data = {"name": "John", "age": 30, "city": "New York"}
        json_str = json.dumps(data)

        result = io.parse_json(json_str)
        assert result == data

    def test_empty_string_raises_error(self):
        """An empty string should raise an error."""
        with pytest.raises(json.JSONDecodeError):
            io.parse_json("")

    def test_invalid_json_string_raises_error(self):
        """An invalid JSON string should raise an error."""
        with pytest.raises(json.JSONDecodeError):
            io.parse_json("{Some string}")

    def test_non_string_input_raises_error(self):
        """A non-string input should raise an error."""
        with pytest.raises(TypeError):
            io.parse_json(None)


class TestParseFile:
    """Test the parse_file function."""

    def test_parse_yaml_file(self, tmp_path: Path):
        with mock.patch("project_forge.core.io.parse_yaml") as mock_parse_yaml:
            mock_parse_yaml.return_value = {"key": "value"}

            test_file_path = tmp_path / "test.yaml"
            test_file_path.write_text("key: value")

            result = io.parse_file(test_file_path)
            assert result == {"key": "value"}
            assert mock_parse_yaml.call_count == 1

    def test_parse_toml_file(self, tmp_path: Path):
        with mock.patch("project_forge.core.io.parse_toml") as mock_parse_toml:
            mock_parse_toml.return_value = {"key": "value"}

            test_file_path = tmp_path / "test.toml"
            test_file_path.write_text('key = "value"')

            result = io.parse_file(test_file_path)
            assert result == {"key": "value"}
            assert mock_parse_toml.call_count == 1

    def test_parse_json_file(self, tmp_path: Path):
        with mock.patch("project_forge.core.io.parse_json") as mock_parse_json:
            mock_parse_json.return_value = {"key": "value"}

            test_file_path = tmp_path / "test.json"
            test_file_path.write_text('{"key": "value"}')

            result = io.parse_file(test_file_path)
            assert result == {"key": "value"}
            assert mock_parse_json.call_count == 1

    def test_unsupported_file_returns_content(self, tmp_path: Path):
        """Parsing an unknown file just returns the file's contents."""
        test_file_path = tmp_path / "test.unsupported"
        test_file_path.write_text("unsupported type file content")
        result = io.parse_file(test_file_path)
        assert result == "unsupported type file content"


class TestMakeSurePathExists:
    """Tests for project_forge.core.io.make_sure_path_exists."""

    def test_creates_missing_directory(self, tmp_path: Path):
        """It creates the path if it does not exist."""
        path_to_create = tmp_path / "test_directory"

        io.make_sure_path_exists(path_to_create)

        assert path_to_create.exists()

    def test_does_nothing_if_directory_exists(self, tmp_path: Path):
        """If the path already exists, nothing is changed."""
        path_to_create = tmp_path / "test_directory"
        Path(path_to_create).mkdir(parents=True, exist_ok=True)
        assert path_to_create.exists()

        io.make_sure_path_exists(path_to_create)
        assert path_to_create.exists()


class TestRemoveSinglePath:
    """Tests for project_forge.core.io.remove_single_path."""

    def test_removes_file(self, tmp_path: Path):
        """It should remove a single file path."""
        path = tmp_path / "file.txt"
        path.touch()
        io.remove_single_path(path)
        assert not path.exists()

    def test_removes_directory(self, tmp_path: Path):
        """It should remove an empty directory path."""
        path = tmp_path / "dir"
        path.mkdir()
        io.remove_single_path(path)
        assert not path.exists()

    def test_removes_directory_with_files(self, tmp_path: Path):
        """It should remove a directory with files in it."""
        dir_path = tmp_path / "dir"
        dir_path.mkdir()
        file_path = dir_path / "file.txt"
        file_path.touch()
        io.remove_single_path(dir_path)
        assert not dir_path.exists()


def test_remove_paths_removes_multiple_paths(tmp_path: Path):
    """It should remove multiple paths."""
    root_dir = tmp_path
    file1 = root_dir / "file1.txt"
    file1.touch()
    file2 = root_dir / "file2.txt"
    file2.touch()
    file3 = root_dir / "file3.txt"
    file3.touch()

    io.remove_paths(root_dir, [Path("file1.txt"), Path("file2.txt"), Path("file3.txt")])

    assert not file1.exists()
    assert not file2.exists()
    assert not file3.exists()
