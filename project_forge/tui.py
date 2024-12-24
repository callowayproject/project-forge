"""A terminal user interface."""

from typing import Any, Callable, Optional

import questionary

from project_forge.core.types import QUESTION_TYPE_CAST, QuestionType


def make_validator(validator_func: Callable) -> Optional[Callable]:
    """Make a questionary validator from a callable."""
    return None


def ask_multiselect(
    prompt: str,
    choices: dict,
    help: Optional[str] = None,
    default: Any = None,
    validator_func: Optional[Callable] = None,
    **kwargs,
) -> list[Any]:
    """Ask a question with multiple answers."""
    question = questionary.checkbox(
        message=prompt,
        choices=choices,
        default=default,
        instruction=help,
        validator=make_validator(validator_func),
        **kwargs,
    )
    responses = question.ask()
    return [choices.get(response, response) for response in responses]


def ask_select(
    prompt: str,
    choices: dict,
    help: Optional[str] = None,
    default: Any = None,
    validator_func: Optional[Callable] = None,
    **kwargs,
) -> Any:
    """Ask a question with multiple choices."""
    question = questionary.select(
        message=prompt,
        choices=choices,
        default=default,
        instruction=help,
        validator=make_validator(validator_func),
        **kwargs,
    )
    response = question.ask()
    return choices.get(response, response)


def ask_question(
    prompt: str,
    type: QuestionType = "str",
    help: Optional[str] = None,
    choices: Optional[dict] = None,
    default: Any = None,
    multiselect: bool = False,
    validator_func: Optional[Callable] = None,
    **kwargs,
) -> Any:
    """Ask the user a question and validate the answer."""
    cast_func = QUESTION_TYPE_CAST.get(type, lambda x: x)  # pragma: no-coverage
    params = {
        "message": prompt,
        "default": default,
        "validate": make_validator(validator_func),
        "multiline": type in {"multiline", "yaml", "json"},
        "instruction": help,
        **kwargs,
    }
    if type == "bool":
        del params["validate"]
        return cast_func(questionary.confirm(**params).ask())
    elif multiselect and choices:
        return [cast_func(item) for item in ask_multiselect(prompt, choices, help, default, validator_func, **kwargs)]
    elif choices:
        return cast_func(ask_select(prompt, choices, help, default, validator_func, **kwargs))
    elif type == "secret":
        del params["default"]
        return questionary.password(**params).ask()
    else:
        params["default"] = str(params["default"]) if params["default"] is not None else ""
        return cast_func(questionary.text(**params).ask())
