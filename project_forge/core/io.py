"""Input/Output operations."""

from pathlib import Path
from typing import Any, Union


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
