"""Caching operations."""

import logging
from pathlib import Path
from tempfile import TemporaryDirectory

from project_forge.core.io import make_sure_path_exists, remove_single_path
from project_forge.core.urls import ParsedURL
from project_forge.git_commands import clone
from project_forge.settings import get_settings

logger = logging.getLogger(__name__)


def get_cache_dir() -> Path:
    """
    Get the path to store cached repos.

    Returns:
        Path to the cache directory or a temporary directory if caching is disabled.
    """
    settings = get_settings()
    if settings.disable_cache:
        with TemporaryDirectory() as temp_dir:
            return Path(temp_dir)
    else:
        make_sure_path_exists(settings.cache_dir)
        return settings.cache_dir


def get_remote_clone(parsed_url: ParsedURL) -> Path:
    """
    Return the path to a locally cloned remote repo.

    This provides some error-checking for the cached repo, and will re-clone if the
    cached repo is in a detached head state.

    Args:
        parsed_url: The parsed Git URL to clone

    Returns:
        The path to the locally cloned repository
    """
    logger.debug(f"Getting cached remote repo {parsed_url.repo_name}")

    cache_dir = get_cache_dir()
    repo_dir = cache_dir.joinpath(parsed_url.repo_name)

    repo = clone(parsed_url, repo_dir)

    if repo.head.is_detached:
        logger.info("The cached repo has a detached head, deleting and re-cloning.")
        remove_single_path(repo_dir)
        clone(parsed_url, repo_dir)

    return repo_dir


def clone_repo(url: ParsedURL) -> Path:
    """
    Clone and cache a Git repository.

    Previously cloned repositories are updated unless they point to a specific reference.

    Args:
        url: The URL to the Git repository

    Returns:
        The full path to the cloned and cached remote repository or the local directory.
    """
    if url.protocol == "file":
        return Path(url.full_path).expanduser().resolve()
    else:
        return get_remote_clone(url)
