"""Functions for using git."""

import logging
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional, Union

from git import GitCommandError, InvalidGitRepositoryError, NoSuchPathError, Repo

from project_forge.core.exceptions import GitError
from project_forge.core.urls import ParsedURL

logger = logging.getLogger(__name__)


def get_repo(
    project_dir: Union[str, Path], search_parent_directories: bool = False, ensure_clean: bool = False
) -> Repo:
    """
    Get the git Repo object for a directory.

    Args:
        project_dir: The directory containing the .git folder
        search_parent_directories: if `True`, all parent directories will be searched for a valid repo as well.
        ensure_clean: if `True`, raise an error if the repo is dirty

    Raises:
        GitError: If the directory is not a git repo
        GitError: If the directory git repository is dirty

    Returns:
        The GitPython Repo object
    """
    try:
        repo = Repo(str(project_dir), search_parent_directories=search_parent_directories)

        if ensure_clean and repo.is_dirty():
            raise GitError("The destination git repository is dirty. Please commit or stash the pending changes.")
        return repo
    except (InvalidGitRepositoryError, NoSuchPathError) as e:
        raise GitError(
            "Some project forge commands only work on git repositories. "
            "Please make the destination directory a git repo."
        ) from e


def clone(repo_url: ParsedURL, dest_path: Optional[Path] = None) -> Repo:
    """
    Clone a repo.

    Args:
        repo_url: The parsed Git repository URL.
        dest_path: The path to clone to.

    Returns:
        The repository.
    """
    dest_path = dest_path or Path.cwd()

    if dest_path.exists():
        logger.debug(f"Found {dest_path}, attempting to update")
        return get_repo(dest_path, ensure_clean=True)
    else:
        logger.debug(f"Cloning {repo_url} into {dest_path}")
        return Repo.clone_from(repo_url.url, dest_path)


def branch_exists(repo: Repo, branch_name: str) -> bool:
    """
    Does the branch exist in the repo?

    Args:
        repo: The repository to check
        branch_name: The name of the branch to check for

    Returns:
        `True` if the branch exists
    """
    return branch_name in repo.refs


def remote_branch_exists(repo: Repo, branch_name: str, remote_name: str = "origin") -> bool:
    """
    Does the branch exist in the remote repo?

    Args:
        repo: The repository to check
        branch_name: The name of the branch to check for
        remote_name: The name of the remote reference. Defaults to `origin`

    Returns:
        `True` if the branch exists in the remote repository
    """
    if remote_name in repo.remotes:
        return branch_name in repo.remotes[remote_name].refs

    return False


def checkout_ref(repo: Repo, ref: str) -> None:
    """
    Checkout a ref.

    Args:
        repo: The repository to check out
        ref: The ref to check out
    """
    repo.git.checkout(ref)


def checkout_branch(repo: Repo, branch_name: str, remote_name: str = "origin") -> None:
    """Checkout a local or remote branch."""
    if repo.is_dirty():
        raise GitError(
            "Project forge cannot apply updates on an unclean git project."
            " Please make sure your git working tree is clean before proceeding."
        )
    if len(repo.remotes) > 0:
        repo.remotes[0].fetch()

    if branch_exists(repo, branch_name):
        repo.heads[branch_name].checkout()
    elif remote_branch_exists(repo, branch_name, remote_name):
        repo.create_head(branch_name, f"origin/{branch_name}")
        repo.heads[branch_name].checkout()
    else:
        repo.create_head(branch_name)
        repo.heads[branch_name].checkout()


def _apply_patch_with_reject(repo: Repo, diff: str) -> None:
    """
    Apply a patch to a destination directory.

    Args:
        repo: The git repo to apply the patch to
        diff: The previously calculated diff
    """
    reject_command = ["git", "apply", "--reject"]
    try:
        logger.info("Attempting to apply patch with rejections.")
        subprocess.run(  # NOQA: S603
            reject_command,
            input=diff.encode(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            check=True,
            cwd=repo.working_dir,
        )
        logger.info("Patch applied successfully.")
    except subprocess.CalledProcessError as e2:
        logger.error(e2.stderr.decode())
        logger.warning(
            "Project directory may have *.rej files reflecting merge conflicts with the update."
            " Please resolve those conflicts manually.",
        )


def apply_patch(repo: Repo, diff: str) -> None:
    """
    Apply a patch to a destination directory.

    A git 3 way merge is the best bet at applying patches.

    Args:
        repo: The git repo to apply the patch to
        diff: The previously calculated diff
    """
    three_way_command = [
        "git",
        "apply",
        "--3way",
        "--whitespace=fix",
    ]

    try:
        logger.info("Attempting to apply patch with 3-way merge.")
        subprocess.run(  # NOQA: S603
            three_way_command,
            input=diff.encode(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            check=True,
            cwd=repo.working_dir,
        )
        logger.info("Patch applied successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"There was a problem with the 3-way merge: {e.stderr.decode()}")
        _apply_patch_with_reject(repo, diff)


@contextmanager
def temp_git_worktree_dir(
    repo_path: Path, worktree_path: Optional[Path] = None, branch: Optional[str] = None, commit: Optional[str] = None
) -> Iterator[Path]:
    """
    Context Manager for a temporary working directory of a branch in a git repo.

    Inspired by https://github.com/thomasjahoda/cookiecutter_project_upgrader/blob/master/
    cookiecutter_project_upgrader/logic.py

    Logic for checking out a branch or commit:

    - If a commit is provided, use that
    - If a branch is provided, and it is not the current branch, use that
    - If a branch is provided, and it is the current branch, use the current commit
    - If neither a branch nor a commit is provided, use the current branch and commit


    Args:
        repo_path: The path to the template git repo
        worktree_path: The path put the worktree in. Defaults to a temporary directory.
        branch: The branch to check out
        commit: The optional commit to check out

    Yields:
        Path: The worktree_path

    Raises:
        GitError: If the worktree could not be created
    """
    # Create a temporary working directory of a branch in a git repo.
    repo = get_repo(repo_path)

    tmp_dir = Path(tempfile.mkdtemp(prefix=repo_path.name))
    worktree_path = worktree_path or tmp_dir
    worktree_path.mkdir(parents=True, exist_ok=True)

    branch_is_active_branch = branch is None or branch == repo.active_branch.name
    git_cmd = ["add", str(worktree_path), commit or branch]
    if branch_is_active_branch and commit is None:
        git_cmd = ["add", "-d", str(worktree_path)]

    try:
        repo.git.worktree(*git_cmd)
        yield Path(worktree_path)
    except GitCommandError as e:
        raise GitError(f"Could not create a worktree for {repo_path}") from e
    finally:
        # Clean up the temporary working directory.
        # Windows has an issue with this:
        #     The process cannot access the file because it is being used by another process
        # Since these will get purged by the OS, I'm not going to worry about determining the problem.
        # remove_single_path(worktree_path)
        # remove_single_path(tmp_dir)
        repo.git.worktree("prune")
