"""General utilities."""

from typing import MutableMapping


def remove_none_values(mapping: MutableMapping) -> dict:
    """
    Removes keys with `None` values from a mapping.

    Args:
        mapping: A dict-like structure

    Returns:
        A new dictionary with no `None` values.
    """
    return {key: val for key, val in mapping.items() if val is not None}
