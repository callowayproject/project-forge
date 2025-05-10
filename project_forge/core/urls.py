"""URL string parsing functions."""

import re
from dataclasses import dataclass
from typing import Dict, NotRequired, TypedDict
from urllib.parse import urlparse

from project_forge.utils import remove_none_values


@dataclass
class ParsedURL:
    """A parsed URL for a git repository."""

    protocol: str = ""
    username: str = ""
    access_token: str = ""
    host: str = ""
    port: str = ""
    full_path: str = ""
    owner: str = ""
    groups_path: str = ""
    repo_name: str = ""
    raw_internal_path: str = ""
    internal_path: str = ""
    checkout: str = ""
    dot_git: str = ""

    @property
    def url(self) -> str:
        """Return the normalized URL string."""
        netloc = self.host
        if self.port:
            netloc += f":{self.port}"
        if self.username:
            if self.access_token:
                netloc = f"{self.username}:{self.access_token}@{netloc}"
            else:
                netloc = f"{self.username}@{netloc}"
        path = f"/{self.owner}/"
        if self.groups_path:
            path += f"{self.groups_path}/"
        path += f"{self.repo_name}{self.dot_git}"
        return f"{self.protocol}://{netloc}{path}"


class PathInfo(TypedDict):
    """Parsed information about a Path."""

    owner: NotRequired[str]
    repo_name: NotRequired[str]
    raw_internal_path: NotRequired[str]
    internal_path: NotRequired[str]
    checkout: NotRequired[str]
    groups_path: NotRequired[str]
    dot_git: NotRequired[str]


GIT_PATH_RE = re.compile(
    r"""(?uix)
    (?P<username>.+?)@
    (?P<domain>[^:/]+)
    (:)?
    (?P<port>[0-9]+)?(?(port))?
    (?P<fullpath>.+)"""
)

PATH_INFO_RE = re.compile(
    r"""(?uix)
    /?
    (?P<owner>[^/]+)/
    (?P<groups_path>.*?)?(?(groups_path)/)?  # Optional group path
    (?P<repo_name>[^/.@#]+)
    (?P<dot_git>\.git)?                      # Optional .git suffix
    (/)?                                     # Optional trailing slash
    (?P<raw_internal_path>(/blob/|/-/blob/|/-/tree/|/tree/|/commit/|@|\#).+)? # Optional /blob/ or /tree/ path
"""
)

INTERNAL_PATH_PREFIX_RE = re.compile(r"(?:/-)?/(tree|commit)/(.+)/?")
PYTHON_PATH_CHECKOUT_RE = re.compile(r"(?:/blob/|/-/blob/)?(?P<internal_path>[^@#]*)(?P<at>@[^#]+)?(?P<hash>#\w+)?")


def parse_internal_path(path: str) -> Dict[str, str]:
    """
    Parse the internal path into internal_path and checkout components.

    Branches or tags with slashes in them will not be able to be parsed out with blobs.

    If the path starts with `/-/tree/`, `/tree/`, or `/commit/`, the remaining are pointers to the entire checkout.
    Otherwise, the path may contain the checkout and the path

    Args:
        path: The raw internal path string.

    Returns:
        A dict with keys `internal_path` and `checkout`.
    """
    output = {"checkout": "", "internal_path": ""}
    if match := INTERNAL_PATH_PREFIX_RE.match(path):
        output["checkout"] = match.group(2).rstrip("/")
    elif match2 := PYTHON_PATH_CHECKOUT_RE.match(path):
        groups = match2.groupdict()
        if internal_path := groups.get("internal_path"):
            output["internal_path"] = internal_path
        if checkout := groups.get("hash") or groups.get("at"):
            output["checkout"] = checkout[1:]
    return output


def parse_git_path(path: str) -> PathInfo:
    """Parse the path from a git URL into components."""
    match = PATH_INFO_RE.match(path)
    default = {"owner": "", "repo_name": "", "raw_internal_path": "", "checkout": "", "groups_path": "", "dot_git": ""}
    if not match:
        return default
    if not match.group("raw_internal_path"):
        match_dict = remove_none_values(match.groupdict())
        return {**default, **match_dict}  # type: ignore[typeddict-item]
    match_dict = remove_none_values(match.groupdict())
    internal_path = remove_none_values(parse_internal_path(match.group("raw_internal_path")))
    return {**default, **match_dict, **internal_path}  # type: ignore[typeddict-item]


# TODO[#4]: Add abbreviation support such as `gh:` and `gl:`


def parse_git_url(git_url: str) -> ParsedURL:
    """Parse a URL string into a `URL` object if it is a valid URL."""
    # Try to parse the URL normally
    bits = urlparse(git_url)

    if bits.scheme:
        full_path = bits.path.rstrip("/")
        if bits.fragment:
            full_path += f"#{bits.fragment}"
        scheme = "file" if bits.scheme in {"file", "a", "b", "c", "d"} else bits.scheme
        url = ParsedURL(
            protocol=scheme,
            username=bits.username or "",
            access_token=bits.password or "",
            host=bits.hostname,
            port=str(bits.port or ""),
            full_path=full_path,
        )
    elif match := GIT_PATH_RE.match(bits.path):
        # It is an ssh URL, so parse the resulting parsed path
        url = ParsedURL(
            protocol="ssh",
            username=match.group("username") or "",
            host=match.group("domain"),
            port=match.group("port") or "",
            full_path=match.group("fullpath").rstrip("/"),
        )
    else:
        url = ParsedURL(protocol="file", full_path=bits.path.rstrip("/"))

    # TODO[#5]: parse_git_path won't work against a file:// scheme. The owner/repo_name will be in different places
    parsed_path = parse_git_path(url.full_path)
    url.owner = parsed_path.get("owner")
    url.repo_name = parsed_path.get("repo_name")
    url.raw_internal_path = parsed_path.get("raw_internal_path")
    url.checkout = parsed_path.get("checkout", "")
    url.internal_path = parsed_path.get("internal_path", "")
    url.dot_git = parsed_path.get("dot_git", "")
    url.groups_path = parsed_path.get("groups_path", "")
    return url
