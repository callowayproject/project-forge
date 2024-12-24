"""Tests for the `project_forge.patterns.paths` module."""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from project_forge.core.exceptions import PathNotFoundError, RepoNotFoundError
from project_forge.models.location import Location, resolve_url_location

VALID_URL = "http://example.com/repo"
VALID_PATH = "/valid/path"


class TestLocation:
    """Tests for the `Location` class."""

    class TestFromString:
        """Tests for the `Location.from_string` class method."""

        def test_recognizes_url_string(self):
            """A URL should be put into the `url` attribute."""
            url = "http://localhost/repo.git"
            location = Location.from_string(url)
            assert location.url == url
            assert location.path is None

        def test_recognizes_path_string(self):
            """A path should be put into the `path` attribute."""
            path = "/local/path"
            location = Location.from_string(path)
            assert location.path == path
            assert location.url is None

        def test_recognizes_git_protocol_string(self):
            """A git protocol should be put into the `url` attribute."""
            url = "git@github.com:user/repo.git"
            location = Location.from_string(url)
            assert location.url == url
            assert location.path is None

        def test_raises_error_for_empty_string(self):
            """An empty string should raise a `ValueError`."""
            with pytest.raises(ValueError):
                Location().from_string("")

    class TestResolve:
        """Tests for the `Location.resolve` method."""

        def test_url_calls_resolve_url_location(self, tmp_path: Path):
            """A location with a URL calls `resolve_url_location`."""
            mocked_resolve_url_location = MagicMock("project_forge.core.location.resolve_url_location")
            location = Location(url="http://localhost/repo.git")
            with patch("project_forge.models.location.resolve_url_location", mocked_resolve_url_location):
                location.resolve()
                mocked_resolve_url_location.assert_called_once_with(location)

        def test_existing_absolute_path_resolves(self, tmp_path: Path):
            """An existing absolute path is resolved to itself."""
            location = Location(path=str(tmp_path))
            assert location.resolve() == tmp_path

        def test_missing_absolute_path_raises_error(self):
            """Attempting to resolve an absolute path that doesn't exist raises a `FileNotFoundError`."""
            path = "/non/existing/absolute/path"
            location = Location(path=path)
            with pytest.raises(PathNotFoundError):
                location.resolve()

        def test_existing_relative_path_with_root_resolves(self, tmp_path: Path):
            """A relative path is resolved using the appropriate root path."""
            path = "./existing/relative/path"
            expected_path = tmp_path.joinpath(Path(path)).resolve()
            expected_path.mkdir(parents=True, exist_ok=True)
            location = Location(path=path)
            assert location.resolve(tmp_path) == expected_path

        def test_existing_relative_path_to_cwd_resolves(self, tmp_path: Path):
            """A relative path is resolved using the current working directory."""
            path = "./existing/relative/path"
            expected_path = tmp_path.joinpath(Path(path)).resolve()
            expected_path.mkdir(parents=True, exist_ok=True)
            location = Location(path=path)
            current_working_directory = Path.cwd()
            os.chdir(tmp_path)
            assert location.resolve(tmp_path) == expected_path
            os.chdir(current_working_directory)

        def test_non_existing_relative_path_raises_error(self, tmp_path: Path):
            path = "./non/existing/relative/path"
            location = Location(path=path)
            with pytest.raises(PathNotFoundError):
                location.resolve(tmp_path)


class TestResolveUrlLocation:
    """Tests for the `resolve_url_location` function."""

    def test_missing_url_attribute_raises_error(self):
        """If the location is missing an `url` attribute, it should raise an error."""
        with pytest.raises(RepoNotFoundError):
            location = Location(path="/")
            _ = resolve_url_location(location)

    def test_location_with_url_and_path_find_path_in_repo(self, tmp_path: Path):
        """If the url and path attributes are set, the result is the path within the cloned repo."""
        # Assemble
        test_location = Location(url=VALID_URL, path=VALID_PATH)
        mocked_clone_repo = MagicMock("project_forge.caching.clone_repo", return_value=tmp_path)
        expected_path = Path(tmp_path).joinpath(VALID_PATH.lstrip("/"))
        expected_path.mkdir(parents=True, exist_ok=True)

        # Act
        with patch("project_forge.caching.clone_repo", mocked_clone_repo):
            result_path = resolve_url_location(test_location)

        # Assert
        assert result_path == expected_path

    def test_location_with_only_url_uses_root_of_repo(self, tmp_path: Path):
        """If there is no `path` attribute, the result is the root of the cloned repo."""
        # Assemble
        test_location = Location(url=VALID_URL)
        mocked_clone_repo = MagicMock("project_forge.caching.clone_repo", return_value=tmp_path)

        # Act
        with patch("project_forge.caching.clone_repo", mocked_clone_repo):
            result_path = resolve_url_location(test_location)

        # Assert
        assert result_path == tmp_path

    def test_missing_file_raises_error(self, tmp_path: Path):
        """If the location doesn't resolve to a local path, it raises an error."""
        # Assemble

        test_location = Location(url=VALID_URL)
        mocked_clone_repo = MagicMock(
            "project_forge.caching.clone_repo", return_value=tmp_path.joinpath("/idontexist")
        )

        # Act
        with patch("project_forge.caching.clone_repo", mocked_clone_repo):
            with pytest.raises(PathNotFoundError):
                result_path = resolve_url_location(test_location)


# TODO[#12]: Test a location with a URL and a relative path with a `../` does not resolve outside the repository
