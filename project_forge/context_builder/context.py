"""Builds and manages the rendering context."""

import datetime
from typing import Callable, Mapping

from project_forge.configurations.composition import Composition
from project_forge.context_builder.data_merge import MERGE_FUNCTION, MergeMethods
from project_forge.context_builder.overlays import process_overlay
from project_forge.rendering.expressions import render_expression


def get_starting_context() -> dict:
    """The starting context for all configurations."""
    return {"now": datetime.datetime.now(tz=datetime.timezone.utc)}


def build_context(composition: Composition, ui: Callable) -> dict:
    """
    Build the context for the composition.

    - set running_context to starting_context (the default from project forge)
    - render composition's extra_context using running_context
    - update running_context with composition's extra_context
    - for each overlay
        - process_overlay
        - update running_context with result of process_overlay

    Args:
        composition: The composition configuration.
        ui: A callable that takes question information and returns the result from the user interface.

    Returns:
        A dictionary
    """
    running_context = get_starting_context()
    for key, value in composition.extra_context.items():
        running_context[key] = render_expression(value, running_context)

    for overlay in composition.overlays:
        overlay_context = process_overlay(overlay, running_context, ui)
        running_context = update_context(composition.merge_keys or {}, running_context, overlay_context)
    return running_context


def update_context(merge_keys: Mapping[str, MergeMethods], left: dict, right: dict) -> dict:
    """Return a dict where the left is updated with the right according to the composition rules."""
    left_keys = set(left.keys())
    right_keys = set(right.keys())
    common_keys = left_keys.intersection(right_keys)
    new_keys = right_keys - common_keys
    result = {}

    for key, value in left.items():
        if key in right:
            merge_func = MERGE_FUNCTION[merge_keys.get(key.lower(), "comprehensive")]
            result[key] = merge_func(value, right[key])
        else:
            result[key] = value

    for key in new_keys:
        result[key] = right[key]

    return result
