"""Tests for `project_forge.utils`."""

import pytest
from pytest import param

from project_forge.core.urls import parse_git_path, parse_git_url, parse_internal_path


@pytest.mark.parametrize(
    ["path", "expected"],
    [
        param(
            "/path/to/repo",
            {"checkout": "", "internal_path": "/path/to/repo"},
            id="does not start with blob, tree, or commit",
        ),
        param("/-/tree/feature/", {"checkout": "feature", "internal_path": ""}, id="/-/tree"),
        param("/tree/feature/", {"checkout": "feature", "internal_path": ""}, id="tree"),
        param("/tree/feature/ABC-111", {"checkout": "feature/ABC-111", "internal_path": ""}, id="slash in checkout"),
        param("/commit/1234567890", {"checkout": "1234567890", "internal_path": ""}, id="commit"),
        param("/-/blob/feature/", {"checkout": "", "internal_path": "feature/"}, id="/-/blob"),
        param("/blob/feature/", {"checkout": "", "internal_path": "feature/"}, id="blob"),
        param("@7921be1", {"checkout": "7921be1", "internal_path": ""}, id="Python version specifier 1"),
        param("@1.3.1#7921be1", {"checkout": "7921be1", "internal_path": ""}, id="Python version specifier 2"),
    ],
)
def test_parse_internal_path(path: str, expected: dict):
    """The `parse_internal_path` function parses checkout components."""
    assert parse_internal_path(path) == expected


@pytest.mark.parametrize(
    ["path", "expected"],
    (
        param(
            "Org/Repo.git",
            {"owner": "Org", "repo_name": "Repo", "dot_git": ".git", "groups": ""},
            id="relative path with .git",
        ),
        param(
            "Org/Repo",
            {"owner": "Org", "repo_name": "Repo", "dot_git": "", "groups": ""},
            id="relative path without .git",
        ),
        param(
            "/Org/Repo.git",
            {"owner": "Org", "repo_name": "Repo", "dot_git": ".git", "groups": ""},
            id="absolute path with .git",
        ),
        param(
            "/Org/Repo",
            {"owner": "Org", "repo_name": "Repo", "dot_git": "", "groups": ""},
            id="absolute path without .git",
        ),
        param(
            "/pypa/pip.git@7921be1",
            {"owner": "pypa", "repo_name": "pip", "dot_git": ".git", "groups": ""},
            id="@ specifier with .git",
        ),
        param(
            "/pypa/pip@7921be1",
            {"owner": "pypa", "repo_name": "pip", "dot_git": "", "groups": ""},
            id="@ specifier without .git",
        ),
        param(
            "/pypa/pip@1.3.1#7921be1",
            {"owner": "pypa", "repo_name": "pip", "dot_git": "", "groups": ""},
            id="# specifier without .git",
        ),
        param(
            "/pypa/pip.git@1.3.1#7921be1",
            {"owner": "pypa", "repo_name": "pip", "dot_git": ".git", "groups": ""},
            id="# specifier with .git",
        ),
        #
        # Group path parsing isn't working. TODO: fix it?
        # param(
        #     "/Org/Group/subGroup/Repo.git/",
        #     {"owner": "Org", "repo_name": "Repo", "dot_git": ".git", "groups": "Group/subGroup/"},
        #     id="Groups",
        # ),
    ),
)
def test_parse_git_path_parses_components(path: str, expected: dict):
    """It should parse the owner, groups, and repo name correctly."""
    result = parse_git_path(path)
    assert result["owner"] == expected["owner"]
    assert result["repo_name"] == expected["repo_name"]
    assert result["groups_path"] == expected["groups"]
    assert result["dot_git"] == expected["dot_git"]


class TestParseGitUrl:
    """Tests for the `parse_git_url` function."""

    @pytest.mark.parametrize(
        ["url", "expected"],
        (
            param("git@github.com:Org/Repo.git", "ssh", id="Git URL no protocol"),
            param("joe@github.com-work:nephila/giturlparse.git", "ssh", id="Git URL no protocol with username"),
            param("git+https://github.com/Org/Repo.git", "git+https", id="Git+Https URL"),
            param("https://github.com/Org/Repo.git", "https", id="HTTPS URL"),
            param("ssh://git@host.org:9999/Org/Repo.git", "ssh", id="SSH URL with protocol"),
            param("git://host.org:9999/Org/Group/subGroup/Repo.git/", "git", id="GIT URL with protocol"),
            param("git+https://github.com/pypa/pip.git@7921be1", "git+https", id="Python version specifier 1"),
            param("git+https://github.com/pypa/pip.git@1.3.1#7921be1", "git+https", id="Python version specifier 2"),
            param("file:///absolute/path/to/repo.git", "file", id="file scheme with absolute path"),
            param("/absolute/path", "file", id="absolute path"),
            param("../relative/path", "file", id="relative path"),
            param("c:/absolute/path", "file", id="absolute path with drive letter"),
        ),
    )
    def test_parses_protocols_correctly(self, url: str, expected: str):
        """Parsing a URL string returns the correct protocol."""
        assert parse_git_url(url).protocol == expected

    @pytest.mark.parametrize(
        ["url", "expected"],
        (
            param("git@github.com:Org/Repo.git", "git", id="git username no protocol"),
            param("joe@github.com-work:Org/Repo.git", "joe", id="non-git username no protocol"),
            param("ssh://git@host.org:9999/Org/Repo.git", "git", id="git username with protocol"),
            param("https://joe:token@gitlab.com/Org/Repo", "joe", id="non-git username with protocol"),
            param("https://gitlab.com/Org/Repo", "", id="no username with protocol"),
        ),
    )
    def test_parses_username_correctly(self, url: str, expected: str):
        """Parsing a URL string returns the correct username."""
        assert parse_git_url(url).username == expected

    @pytest.mark.parametrize(
        ["url", "expected"],
        (
            param("git@github.com:Org/Repo.git", "github.com", id="git protocol"),
            param("git@host.org:9999/Org/Repo.git", "host.org", id="git protocol with port"),
            param("joe@github.com-work:Org/Repo.git", "github.com-work", id="git protocol, odd domain"),
            param("ssh://git@host.org:9999/Org/Repo.git", "host.org", id="has username and port"),
            param("https://joe:token@gitlab.com/Org/Repo", "gitlab.com", id="has username and password"),
            param("https://gitlab.com/Org/Repo", "gitlab.com", id="basic"),
        ),
    )
    def test_parses_domain_correctly(self, url: str, expected: str):
        """Parsing a URL string returns the correct domain."""
        assert parse_git_url(url).host == expected

    @pytest.mark.parametrize(
        ["url", "expected"],
        (
            param("git@github.com:Org/Repo.git", "Org/Repo.git", id="git protocol"),
            param("git@github.com:9999/Org/Repo.git", "/Org/Repo.git", id="git protocol with port"),
            param("https://github.com/Org/Repo.git", "/Org/Repo.git", id="HTTPS URL"),
            param(
                "git+https://github.com/pypa/pip.git@7921be1", "/pypa/pip.git@7921be1", id="Python version specifier 1"
            ),
            param(
                "git+https://github.com/pypa/pip.git@1.3.1#7921be1",
                "/pypa/pip.git@1.3.1#7921be1",
                id="Python version specifier 2",
            ),
        ),
    )
    def test_parses_full_path_correctly(self, url: str, expected: str):
        """Parsing a URL string returns the correct full path."""
        assert parse_git_url(url).full_path == expected


@pytest.mark.parametrize(
    ["initial_url", "expected"],
    [
        param(
            "git+https://github.com/pypa/pip.git@7921be1",
            "git+https://github.com/pypa/pip.git",
            id="Python version specifier 1",
        ),
        param(
            "git+https://github.com/pypa/pip.git@1.3.1#7921be1",
            "git+https://github.com/pypa/pip.git",
            id="Python version specifier 2",
        ),
        param(
            "joe@github.com-work:Org/Repo.git", "ssh://joe@github.com-work/Org/Repo.git", id="git protocol, odd domain"
        ),
        param(
            "ssh://git@host.org:9999/Org/Repo.git", "ssh://git@host.org:9999/Org/Repo.git", id="has username and port"
        ),
        param(
            "https://joe:token@gitlab.com/Org/Repo",
            "https://joe:token@gitlab.com/Org/Repo",
            id="has username and password",
        ),
        param(
            "git://host.org:9999/Org/Repo.git/",
            "git://host.org:9999/Org/Repo.git",
            id="Git URL with protocol",
        ),
    ],
)
def test_reformed_url_does_not_mutate_url(initial_url: str, expected: str):
    """The URL.url function should produce the correct url."""
    url = parse_git_url(initial_url)
    assert url.url == expected
