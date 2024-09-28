"""Caching operations."""

from pathlib import Path
from typing import Optional


def cached_repo_name(repo_url: str, checkout: Optional[str] = None) -> str:
    """Construct the destination repo name from the repo URL and checkout."""
    repo_name = repo_url.rstrip("/").rsplit("/", 1)[-1]  # Get the last part of the URL path
    repo_name = repo_name.rsplit(".git")[0]  # Strip off any .git suffix
    if checkout is not None:
        repo_name = f"{repo_name}_{checkout}"
    return repo_name


def clone_repo(url: str) -> Path:
    """
    Clone and cache a Git repository.

    Previously cloned repositories are updated unless they point to a specific reference.

    Args:
        url: The URL to the Git repository

    Returns:
        The full path to the cloned and cached
    """
    # TODO: implement this
    # raise NotImplementedError
    pass
