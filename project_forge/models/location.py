"""Models core to the project forge package."""

from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel, Field, model_validator

from project_forge import caching
from project_forge.core.exceptions import PathNotFoundError, RepoNotFoundError
from project_forge.core.urls import ParsedURL, parse_git_url


class Location(BaseModel):
    """
    The location of a file or directory.

    A location supports referencing the file or directory using:

    - relative path
    - absolute path
    - git URL
    - git URL plus revision/tag/branch plus path in the repo

    When `url` is specified, the `path` is relative to the root of the repository.

    At least one of `path` or `url` must be specified.
    """

    path: Optional[str] = Field(default=None, description="The relative or absolute path to the location.")
    url: Optional[str] = Field(default=None, description="The Git URL to the location.")
    _resolved_path: Optional[Path] = None
    _parsed_url: Optional[ParsedURL] = None

    @classmethod
    def from_string(cls, location: str) -> "Location":
        """Convert a path or URL string into a location."""
        if location.startswith("http") or location.startswith("git"):
            return cls(url=location)
        else:
            return cls(path=location)

    @model_validator(mode="before")
    @classmethod
    def _process_url(cls, values: dict) -> dict:
        """Parse the URL, and modify the `path` if the URL is a local path."""
        if not values.get("url"):
            return values

        parsed_url = parse_git_url(values["url"])
        if parsed_url.protocol == "file":
            path = Path(parsed_url.full_path, values.get("path", ""))
            values["path"] = str(path)
            values["url"] = None

        return values

    @model_validator(mode="after")
    def _ensure_path_or_url(self) -> "Location":
        """Make sure that at least one of `path` or `url` is specified."""
        if not any([self.path is not None, self.url is not None]):
            raise ValueError("At least one of `path` or `url` must be specified.")
        return self

    @property
    def parsed_url(self) -> Optional[ParsedURL]:
        """Parse the URL and cache it."""
        if self.url and not self._parsed_url:
            self._parsed_url = parse_git_url(self.url)
        return self._parsed_url

    def resolve(self, root_path: Optional[Path] = None) -> Path:
        """
        Find the proper template path for a pattern.

        - A relative `path` is relative to the root path and must exist.
        - An absolute `path` must exist.
        - A URL must be to a git repository and a `path` must exist within the repository.

        Args:
            root_path: The path to use for resolving relative `path`s if there is no `url`.
                The current working directory is used if None.

        Raises:
            RepoNotFound: If the URL provided returns a 404 error
            RepoAuthError: If the URL provided returns a 401 or 403 error
            PathNotFound: If the path was not found

        Returns:
            The path to the location
        """
        if self._resolved_path:
            return self._resolved_path

        if self.parsed_url:
            self._resolved_path = resolve_url_location(self)
            return self._resolved_path

        template_path = make_absolute(self.path, root_path)

        if not template_path.exists():
            raise PathNotFoundError(f"The path {template_path} was not found.")
        self._resolved_path = template_path
        return self._resolved_path

    def __eq__(self, other: object) -> bool:
        """
        Compare if the objects are the same.

        This ignores the private attribute `_resolved_path`. The locations are equal regardless if the `resolve` method
        was previously called.

        Args:
            other: The other object to compare to.

        Returns:
            True if the objects are the same, False otherwise.
        """
        if not isinstance(other, Location):
            return False
        return self.path == other.path and self.url == other.url


def make_absolute(path: Union[str, Path], root_path: Optional[Path] = None) -> Path:
    """
    Convert relative paths to absolute paths, and return absolute paths unchanged.

    Args:
        path: The path to convert.
        root_path: The root path to resolve relative paths against.

    Returns:
        An absolute path.
    """
    template_path = Path(path)
    if template_path.is_absolute():
        return template_path

    root_path = root_path or Path.cwd()
    root_path = root_path.parent if root_path.is_file() else root_path
    return root_path.joinpath(template_path).resolve()


def resolve_url_location(location: Location) -> Path:
    """
    Cache the URL and return the Path to the resolved location.

    This downloads the repo into a cache and returns the full path to the template dir.

    Args:
        location: The location object with a parsed URL

    Raises:
        RepoNotFound: If the URL provided returns a 404 error
        RepoAuthError: If the URL provided returns a 401 or 403 error
        PathNotFound: If the path was not found

    Returns:
        Path to the template dir
    """
    if not location.parsed_url:
        raise RepoNotFoundError("A URL must be provided.")

    cached_repo_path = caching.clone_repo(location.parsed_url)
    path = location.path.lstrip("/") if location.path else ""
    full_template_path = cached_repo_path.joinpath(path)

    if not full_template_path.exists():
        raise PathNotFoundError(f"The path {path} is not in the repository {location.url}.")

    return full_template_path
