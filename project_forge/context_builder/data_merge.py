"""Tools for merging data."""

import copy
import logging
from collections import OrderedDict
from functools import reduce
from typing import Any, Iterable, Literal, MutableMapping, TypeVar, overload

from immutabledict import immutabledict

logger = logging.getLogger(__name__)

T = TypeVar("T")


@overload
def freeze_data(obj: set | frozenset) -> frozenset: ...


@overload
def freeze_data(obj: tuple | list) -> tuple: ...


@overload
def freeze_data(obj: dict | OrderedDict | immutabledict) -> immutabledict: ...


@overload
def freeze_data(obj: str) -> str: ...


@overload
def freeze_data(obj: int) -> int: ...


@overload
def freeze_data(obj: float) -> float: ...


@overload
def freeze_data(obj: bytes) -> bytes: ...


def freeze_data(obj: Any) -> Any:
    """Check type and recursively return a new read-only object."""
    if isinstance(obj, (str, int, float, bytes, type(None), bool)):
        return obj
    elif isinstance(obj, tuple) and type(obj) is not tuple:  # assumed namedtuple
        return type(obj)(*(freeze_data(i) for i in obj))
    elif isinstance(obj, (tuple, list)):
        return tuple(freeze_data(i) for i in obj)
    elif isinstance(obj, (dict, OrderedDict, immutabledict)):
        return immutabledict({k: freeze_data(v) for k, v in obj.items()})
    elif isinstance(obj, (set, frozenset)):
        return frozenset(freeze_data(i) for i in obj)
    raise ValueError(obj)


def merge_iterables(iter1: Iterable, iter2: Iterable) -> set:
    """
    Merge and de-duplicate a bunch of lists into a single list.

    Order is not guaranteed.

    Args:
        iter1: An Iterable
        iter2: An Iterable

    Returns:
        The merged, de-duplicated sequence as a set
    """
    from itertools import chain

    return set(chain(freeze_data(iter1), freeze_data(iter2)))


def update(left_val: T, right_val: T) -> T:
    """Do a `dict.update` on all the dicts."""
    match left_val, right_val:
        case (dict(), dict()):
            return left_val | right_val  # type: ignore[return-value]
        case _:
            return right_val


def nested_overwrite(*dicts: dict) -> dict:
    """
    Merges dicts deeply.

    Args:
        *dicts: List of dicts to merge with the first one as the base

    Returns:
        dict: The merged dict
    """

    def merge_into(d1: dict, d2: dict) -> dict:
        for key, value in d2.items():
            if key not in d1 or not isinstance(d1[key], dict):
                d1[key] = copy.deepcopy(value)
            else:
                d1[key] = merge_into(d1[key], value)
        return d1

    return reduce(merge_into, dicts, {})


def comprehensive_merge(left_val: T, right_val: T) -> T:
    """
    Merges data comprehensively.

    All arguments must be of the same type.

    - Scalars are overwritten by the new values
    - lists are merged and de-duplicated
    - dicts are recursively merged

    Args:
        left_val: The item to merge into
        right_val: The item to merge from

    Returns:
        The merged data
    """
    dict_types = (dict, OrderedDict, immutabledict)
    iterable_types = (list, set, tuple)

    def merge_into(d1: Any, d2: Any) -> Any:
        if isinstance(d1, dict_types) and isinstance(d2, dict_types):
            if isinstance(d1, OrderedDict) or isinstance(d2, OrderedDict):
                od1: MutableMapping[Any, Any] = OrderedDict(d1)
                od2: MutableMapping[Any, Any] = OrderedDict(d2)
            else:
                od1 = dict(d1)
                od2 = dict(d2)

            for key in od2:
                od1[key] = merge_into(od1[key], od2[key]) if key in od1 else copy.deepcopy(od2[key])
            return od1  # type: ignore[return-value]
        elif isinstance(d1, list) and isinstance(d2, iterable_types):
            return list(merge_iterables(d1, d2))
        elif isinstance(d1, set) and isinstance(d2, iterable_types):
            return merge_iterables(d1, d2)
        elif isinstance(d1, tuple) and isinstance(d2, iterable_types):
            return tuple(merge_iterables(d1, d2))
        else:
            return copy.deepcopy(d2)

    return merge_into(left_val, right_val)


# Strategies merging data.
MergeMethods = Literal["overwrite", "comprehensive"]

UPDATE = "update"
"""Overwrite at the top level like `dict.update()`."""

COMPREHENSIVE = "comprehensive"
"""Comprehensively merge the two data structures.

- Scalars are overwritten by the new values
- lists are merged and de-duplicated
- dicts are recursively merged
"""

MERGE_FUNCTION = {
    COMPREHENSIVE: comprehensive_merge,
    UPDATE: update,
}
