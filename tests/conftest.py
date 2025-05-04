"""Configuration and utilities for PyTest."""

import sys
from pathlib import Path

import pytest
from git import Actor, Repo

pytest_plugins = ["pytester", "forger"]


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    """Provide the path to the fixture directory."""
    tests_dir = Path(__file__).parent
    return tests_dir / "fixtures"


skip_if_windows = pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows yet")


@pytest.fixture
def default_origin(tmp_path: Path) -> Repo:
    """Create a default origin repo."""
    tmp_repo_path = tmp_path / "tmp_repo"
    tmp_repo = Repo.init(tmp_repo_path)
    configparser = tmp_repo.config_writer("repository")
    configparser.set_value("commit", "gpgsign", False)
    configparser.set_value("tag", "gpgsign", False)
    configparser.release()
    tmp_repo_path.joinpath("README.md").write_text("Hello World!")
    tmp_repo.index.add(["README.md"])
    tmp_repo.index.commit(
        message="new: first commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-01 10:00:00"
    )
    tmp_repo_path.joinpath("README.md").write_text("Hello World!\n\nThis is a test.")
    tmp_repo.index.add(["README.md"])
    tmp_repo.index.commit(
        message="second commit", committer=Actor("Bob", "bob@example.com"), commit_date="2022-01-01 11:00:00"
    )
    tmp_repo.create_tag("v1.0.0")
    tmp_repo.create_head("remote-branch")
    tmp_repo.heads["remote-branch"].checkout()
    tmp_repo_path.joinpath("newfile.md").write_text("Hello World!\n\nThis is a test.\n\nThis is a new line.")
    tmp_repo.index.add(["newfile.md"])
    tmp_repo.index.commit(
        message="first commit on a branch",
        committer=Actor("Bob", "bob@example.com"),
        commit_date="2022-01-01 12:00:00",
    )
    origin_path = tmp_path / "origin.git"
    origin = Repo.init(origin_path, bare=True)

    tmp_repo.create_remote("origin", str(origin_path))
    tmp_repo.remotes.origin.push("master")
    tmp_repo.remotes.origin.push("remote-branch")
    tmp_repo.remotes.origin.push("v1.0.0")

    return origin


@pytest.fixture
def default_repo(default_origin: Repo, tmp_path: Path) -> Repo:
    """Clone the default origin repo."""
    repo = default_origin.clone(tmp_path / "repo")
    repo.heads.master.checkout()
    repo.remotes.origin.pull()
    configparser = repo.config_writer("repository")
    configparser.set_value("commit", "gpgsign", False)
    configparser.set_value("tag", "gpgsign", False)
    configparser.release()

    return repo


@pytest.fixture
def temp_directory(tmp_path: Path) -> Path:
    """Fixture to provide a temporary directory for testing."""
    temp_dir = tmp_path / "subdir"
    temp_dir.mkdir()
    return temp_dir
