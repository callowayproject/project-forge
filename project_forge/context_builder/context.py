"""Builds and manages the rendering context."""

import datetime
from typing import Callable, Mapping, Optional

from project_forge.context_builder.data_merge import MERGE_FUNCTION, MergeMethods
from project_forge.context_builder.overlays import process_overlay
from project_forge.context_builder.tasks import process_task
from project_forge.models.composition import Composition
from project_forge.models.overlay import Overlay
from project_forge.models.task import Task
from project_forge.rendering.expressions import render_expression


def get_starting_context() -> dict:
    """The starting context for all configurations."""
    return {"now": datetime.datetime.now(tz=datetime.timezone.utc)}


def build_context(composition: Composition, ui: Callable, initial_context: Optional[dict] = None) -> dict:
    """
    Build the context for the composition.

    - set running_context to starting_context (the default from project forge)
    - render composition's extra_context using running_context
    - update running_context with composition's extra_context
    - for each overlay
        - process_overlay
        - update running_context with the result of process_overlay

    Args:
        composition: The composition configuration.
        ui: A callable that takes question information and returns the result from the user interface.
        initial_context: The initial context to add to the context.

    Returns:
        A dictionary
    """
    running_context = get_starting_context()
    initial_context = initial_context or {}
    for key, value in {**composition.extra_context, **initial_context}.items():
        running_context[key] = render_expression(value, running_context)

    for step in composition.steps:
        match step:
            case Overlay():
                updated_context = process_overlay(step, running_context, ui)
            case Task():
                updated_context = process_task(step, running_context)
            case _:
                updated_context = {}
        running_context = update_context(composition.merge_keys or {}, running_context, updated_context)
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
