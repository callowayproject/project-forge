"""Core exceptions."""


class ProjectForgeError(Exception):
    """Base exception for all Project Forge errors."""

    pass


class RepoNotFoundError(ProjectForgeError):
    """The URL to a repo location was not found."""

    pass


class RepoAuthError(ProjectForgeError):
    """The URL to a repo location gave an authentication error."""

    pass


class PathNotFoundError(ProjectForgeError):
    """The location path was not found."""

    pass


class GitError(ProjectForgeError):
    """There was a problem doing git operations."""

    pass


class RenderError(ProjectForgeError):
    """There was a problem rendering a template."""

    pass
