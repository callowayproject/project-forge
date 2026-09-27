"""Compile the context from all the overlays."""

from copy import deepcopy
from typing import Any, Callable, MutableMapping

from project_forge.context_builder.questions import answer_question
from project_forge.models.overlay import Overlay
from project_forge.rendering.expressions import render_expression


def process_overlay(overlay: Overlay, running_context: dict[str, Any], question_ui: Callable) -> dict[str, Any]:
    """
    Get the context from an overlay.

    - update overlay pattern's extra_context with overlay's extra_context
    - render extra_context with running_context
    - update running_context with extra_context
    - for each question in pattern
        - set response to the result of answer_question
        - update running context with response
    - re-render the pattern's extra_context, now that questions are answered

    Contract: overlay ``extra_context`` values are rendered once, before questions are asked, so
    they must not reference question answers. Pattern ``extra_context`` values are rendered twice
    (before and after questions) so that they may reference question answers.

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
    force_default = not overlay.ask_questions

    for question in pattern.questions:
        if force_default:
            question.force_default = True
        current_context.update(
            answer_question(
                question=question,
                running_context=current_context,
                question_ui=question_ui,
                answer_map=overlay.answer_map,
                default_overrides=overlay.defaults,
            )
        )

    return render_pattern_context_after_questions(current_context, pattern.extra_context)


def render_pattern_context_after_questions(context: MutableMapping, pattern_context: MutableMapping) -> dict:
    """
    Re-render the pattern's extra_context now that questions have been answered.

    Pattern extra_context values may be Jinja expressions referencing question answers (e.g.
    ``package_path = "{{ repo_name }}/{{ package_name }}"``), which don't exist yet when
    `merge_contexts` first renders them in `process_overlay`. This re-render pass makes those
    values resolve correctly. Overlay extra_context is intentionally excluded here: it is rendered
    only once, before questions, and must not depend on answers.

    Args:
        context: The running context, including question answers, to render against and update.
        pattern_context: The pattern's extra_context mapping.

    Returns:
        The context with pattern extra_context re-rendered.
    """
    return merge_contexts(context, {}, pattern_context)


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
        if isinstance(value, str):
            out_context[key] = render_expression(value, out_context)
        else:
            out_context[key] = value
    return dict(out_context)
