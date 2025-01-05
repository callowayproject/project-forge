"""Preparation for getting answers for questions."""

from typing import Any, Callable, Dict, List, Optional

from project_forge.core.validators import ExprValidator
from project_forge.models.pattern import Choice, Question
from project_forge.rendering.expressions import render_bool_expression, render_expression


def filter_choices(choices: List[Choice], running_context: dict) -> dict:
    """
    Filter the choices to a question using the running context.

    - for each choice
        - render `skip_when` using running_context
        - if skip_when
            - don't include the choice in the dictionary
        - else
            - add the label->value to the dictionary

    Args:
        choices: A list of choice objects that require filtering
        running_context: The context used for rendering skip_when expressions

    Returns:
        The dictionary of valid label->value choices.
    """
    result = {}
    for choice in choices:
        skip_when = render_bool_expression(choice.skip_when, running_context) if choice.skip_when else False
        if not skip_when:
            result[choice.label] = (
                render_expression(choice.value, running_context) if isinstance(choice.value, str) else choice.value
            )
    return result


def answer_question(
    question: Question,
    running_context: dict,
    question_ui: Callable,
    answer_map: Optional[dict] = None,
    default_overrides: Optional[dict] = None,
) -> Dict[str, Any]:
    """
    Determine the answer to a question.

    - if question name in overlay's answer_map
        - return answer_map[question_name]
    - Update default with overlay's default (if it exists)
    - Render default using running_context
    - render `force_default` using running_context
    - if force_default
        - return default
    - else
        - return response from send question information to user interface

    Args:
        question: The question configuration.
        running_context: The current running context used for rendering defaults, answer mappings, and when conditions.
        question_ui: A callable that takes question information and returns the result from the user interface.
        answer_map: A mapping of question keys to answers.
        default_overrides: A mapping of question keys to default values.

    Returns:
        A dictionary with the question's name -> value
    """
    answer_map = answer_map or {}
    if question.name in answer_map:
        return {question.name: render_expression(answer_map[question.name], running_context)}

    if question.name in running_context:
        return {question.name: running_context[question.name]}

    default_overrides = default_overrides or {}
    if question.name in default_overrides:
        default = render_expression(default_overrides[question.name], running_context)
    else:
        default = render_expression(question.default, running_context) if question.default else None

    if render_bool_expression(question.force_default or "False", running_context):
        return {question.name: default}

    answer = question_ui(
        prompt=question.prompt,
        type=question.type,
        help=question.help,
        choices=filter_choices(question.choices, running_context),
        default=default,
        multiselect=question.multiselect,
        validator_func=ExprValidator(question.validator),
    )
    return {question.name: answer}
