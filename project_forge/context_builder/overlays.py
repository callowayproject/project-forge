"""Compile the context from all the overlays."""

from copy import deepcopy
from typing import Callable, MutableMapping

from project_forge.configurations.composition import Overlay
from project_forge.context_builder.questions import answer_question
from project_forge.rendering import render_expression


def process_overlay(overlay: Overlay, running_context: dict, question_ui: Callable) -> dict:
    """
    Get the context from an overlay.

    - update overlay pattern's extra_context with overlay's extra_context
    - render extra_context with running_context
    - update running_context with extra_context
    - for each question in pattern
        - set response to result of answer_question
        - update running context with response

    Args:
        overlay: The overlay configuration.
        running_context: The current running context used for rendering defaults, answer mappings, and when conditions.
        question_ui: A callable that takes question information and returns the result from the user interface.

    Returns:
        A new running context that is the combination of the initial running context, the extra contexts
        from the overlay and pattern, and the answers to the questions.
    """
    current_context = deepcopy(running_context)
    pattern = overlay.pattern
    current_context = merge_contexts(current_context, overlay.extra_context, pattern.extra_context)

    for question in pattern.questions:
        current_context.update(
            answer_question(
                question=question,
                running_context=current_context,
                question_ui=question_ui,
                answer_map=overlay.answer_map,
                default_overrides=overlay.defaults,
            )
        )

    return current_context


def merge_contexts(
    initial_context: MutableMapping, overlay_context: MutableMapping, pattern_context: MutableMapping
) -> dict:
    """
    Merge contexts together and render the values.

    The overlay context values will override the pattern context values.

    Args:
        initial_context: The initial context to be updated
        overlay_context: The extra context from the overlay
        pattern_context: The extra context from the pattern

    Returns:
        The merged and rendered context
    """
    out_context = deepcopy(initial_context)
    extra_context = {**pattern_context, **overlay_context}
    for key, value in extra_context.items():
        out_context[key] = render_expression(value, out_context)
    return dict(out_context)
