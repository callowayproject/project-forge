"""Core exceptions."""


class RepoNotFoundError(Exception):
    """The URL to a repo location was not found."""

    pass


class RepoAuthError(Exception):
    """The URL to a repo location gave an authentication error."""

    pass


class PathNotFoundError(Exception):
    """The location path was not found."""

    pass
