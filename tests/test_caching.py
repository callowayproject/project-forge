"""Tests for project_forge.caching."""

from pathlib import Path
from unittest.mock import MagicMock, patch
from project_forge.caching import get_cache_dir, get_remote_clone, clone_repo
import pytest

from project_forge.core.urls import ParsedURL, parse_git_url


class TestGetCacheDir:
    """Tests for the `get_cache_dir` function."""

    @patch("project_forge.caching.get_settings")
    @patch("project_forge.caching.TemporaryDirectory")
    def test_returns_temporary_directory_if_cache_disabled(self, mock_temp_dir, mock_get_settings):
        """When caching is disabled, the function returns a temporary directory path."""
        # Assemble
        mock_settings = MagicMock()
        mock_settings.disable_cache = True
        mock_temp_dir.return_value.__enter__.return_value = "/temporary"
        mock_get_settings.return_value = mock_settings

        # Act
        cache_dir = get_cache_dir()

        # Assert
        mock_temp_dir.assert_called_once()
        assert cache_dir == Path("/temporary")

    @patch("project_forge.caching.get_settings")
    @patch("project_forge.caching.make_sure_path_exists")
    def test_returns_cache_directory_if_cache_enabled(self, mock_make_sure_path_exists, mock_get_settings):
        """When caching is enabled, it returns the path to the caching directory."""
        # Assemble
        mock_settings = MagicMock()
        mock_settings.disable_cache = False
        mock_settings.cache_dir = Path("/cache")
        mock_get_settings.return_value = mock_settings

        # Act
        cache_dir = get_cache_dir()

        # Assert
        mock_make_sure_path_exists.assert_called_once_with(mock_settings.cache_dir)
        assert cache_dir == mock_settings.cache_dir


class TestGetRemoteClone:
    """Tests for the `get_remote_clone` function."""

    @patch("project_forge.caching.get_cache_dir", return_value=Path("/tmp/cache"))
    @patch("project_forge.caching.clone")
    @patch("project_forge.caching.remove_single_path")
    def test_repo_is_cloned_once_if_not_detached(self, mock_remove_single_path, mock_clone, mock_get_cache_dir):
        """When the head is not detached, the repo is only cloned once."""
        # Assemble
        ParsedURL = MagicMock()
        ParsedURL.repo_name = "my_test_repo"
        repo = MagicMock()
        repo.head.is_detached = False
        mock_clone.return_value = repo

        # Act
        result = get_remote_clone(ParsedURL)

        # Assert
        assert result == Path("/tmp/cache/my_test_repo")
        mock_clone.assert_called_with(ParsedURL, Path("/tmp/cache/my_test_repo"))
        mock_remove_single_path.assert_not_called()

    @patch("project_forge.caching.get_cache_dir", return_value=Path("/tmp/cache"))
    @patch("project_forge.caching.clone")
    @patch("project_forge.caching.remove_single_path")
    def test_repo_is_cloned_twice_if_detached(self, mock_remove_single_path, mock_clone, mock_get_cache_dir):
        """If the head is detached, the repo is cloned, deleted, and cloned again."""
        # Assemble
        ParsedURL = MagicMock()
        ParsedURL.repo_name = "my_test_repo"
        repo = MagicMock()
        repo.head.is_detached = True
        mock_clone.return_value = repo

        # Act
        result = get_remote_clone(ParsedURL)

        # Assert
        assert result == Path("/tmp/cache/my_test_repo")
        assert mock_remove_single_path.call_count == 1
        assert mock_clone.call_count == 2


class TestCloneRepo:
    """Tests for the `clone_repo` function."""

    @pytest.mark.parametrize("url_path", ["/path/to/repo", "~/path/to/repo"])
    def test_file_protocol_returns_local_path(self, url_path: str):
        """ParsedURLs with file:// protocols return the local path."""
        # Assemble
        url = ParsedURL(protocol="file", full_path=url_path)

        # Act
        result = clone_repo(url)

        # Assert
        assert result == Path(url_path).expanduser().resolve(), "Cloned repository path did not match expected."

    @pytest.mark.parametrize("url_path", ["https://github.com/user/repo", "git://github.com/user/repo.git"])
    def test_clones_remote_protocols(self, url_path: str):
        """The function delegates to the get_remote_clone function for non-file protocols."""
        # Assemble
        url = parse_git_url(url_path)

        # Act
        with patch(
            "project_forge.caching.get_remote_clone", return_value=Path("/path/to/cloned/repo")
        ) as mock_get_remote_clone:
            result = clone_repo(url)

        # Assert
        mock_get_remote_clone.assert_called_once_with(url), "Expected get_remote_clone to be called."
        assert result == mock_get_remote_clone.return_value, "Result did not match expected cloned repository path."
