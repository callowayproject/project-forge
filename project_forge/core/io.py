"""Input/Output operations."""

import logging
import os
import stat
from pathlib import Path
from typing import Any, Callable, Iterable, Union

from project_forge.core.exceptions import ProjectForgeError

logger = logging.getLogger(__name__)


def parse_yaml(contents: str) -> Any:
    """Parse a YAML string into a data structure."""
    import yaml

    return yaml.load(contents, Loader=yaml.SafeLoader)


def parse_toml(contents: str) -> Any:
    """Parse a TOML string into a data structure."""
    import tomlkit

    return tomlkit.loads(contents).unwrap()


def parse_json(contents: str) -> Any:
    """Parse a JSON string into a data structure."""
    import json

    return json.loads(contents)


def parse_file(path: Union[str, Path]) -> Any:
    """
    Read a file and parse its contents.

    The file's extension will be used to determine the file type, and the return type.

    Args:
        path: The path to the file to read

    Returns:
        A data structure (from YAML, TOML, JSON) or a string.
    """
    path = Path(path)
    file_type = path.suffix[1:]
    contents = path.read_text(encoding="utf-8")

    if file_type == "yaml":
        return parse_yaml(contents)
    elif file_type == "toml":
        return parse_toml(contents)
    elif file_type == "json":
        return parse_json(contents)
    else:
        return contents


def make_sure_path_exists(path: "os.PathLike[str]") -> None:
    """
    Ensure that a directory exists, creating it if it does not.

    Args:
        path: A directory tree path for creation.

    Raises:
        ProjectForgeError: When there is an OSError
    """
    logger.debug(f"Making sure path exists (creates tree if not exist): {path}")
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
    except OSError as e:  # pragma: no-coverage
        raise ProjectForgeError(f"Unable to create directory at {path}") from e


def remove_paths(root: Path, paths_to_remove: Iterable[Path]) -> None:
    """
    Remove all paths in `paths_to_remove` from `root`.

    Nabbed from Cruft: https://github.com/cruft/cruft/

    Args:
        root: The absolute path of the directory requiring path removal
        paths_to_remove: The set of relative paths to remove from `root`
    """
    # There is some redundancy here in chmod-ing dirs and/or files differently.
    abs_paths_to_remove = [root / path_to_remove for path_to_remove in paths_to_remove]

    for path in abs_paths_to_remove:
        remove_single_path(path)


def remove_readonly_bit(func: Callable[[str], None], path: str, _: Any) -> None:  # pragma: no-coverage
    """Clear the readonly bit and reattempt the removal."""
    os.chmod(path, stat.S_IWRITE)  # WINDOWS
    func(path)


def remove_single_path(path: Path) -> None:
    """
    Remove a path with extra error handling for Windows.

    Args:
        path: The path to remove

    Raises:
        IOError: If the file could not be removed
    """
    from shutil import rmtree

    if path.is_dir():
        try:
            rmtree(path, ignore_errors=False, onerror=remove_readonly_bit)
        except Exception as e:  # pragma: no-coverage
            raise IOError("Failed to remove directory.") from e
    try:
        path.unlink()
    except FileNotFoundError:  # pragma: no-coverage
        pass
    except PermissionError:  # pragma: no-coverage
        path.chmod(stat.S_IWRITE)
        path.unlink()
    except Exception as exc:  # pragma: no-coverage
        raise IOError("Failed to remove file.") from exc
