"""Builds and manages the rendering context."""

import datetime
from typing import Callable

from project_forge.configurations.composition import Composition
from project_forge.context_builder.overlays import process_overlay
from project_forge.rendering import render_expression


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
        running_context.update(process_overlay(overlay, running_context, ui))
    return running_context
