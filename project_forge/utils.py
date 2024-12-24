"""General utilities."""

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, MutableMapping


def remove_none_values(mapping: MutableMapping) -> dict:
    """
    Removes keys with `None` values from a mapping.

    Args:
        mapping: A dict-like structure

    Returns:
        A new dictionary with no `None` values.
    """
    return {key: val for key, val in mapping.items() if val is not None}


@contextmanager
def inside_dir(dir_path: Path) -> Generator[None, None, None]:
    """
    Temporarily switch the current directory to the given path.

    Args:
        dir_path: path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dir_path)
        yield
    finally:
        os.chdir(old_path)
