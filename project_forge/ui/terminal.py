"""A terminal user interface."""

from typing import Any, Callable, Optional, Union

import questionary

from project_forge.core.types import QUESTION_TYPE_CAST, QuestionType


def make_validator(validator_func: Optional[Callable]) -> Callable:
    """Make a questionary validator from a callable that raises ValueError on invalid input."""
    if validator_func is None:
        return lambda value: True

    def validate(value: Any) -> Union[bool, str]:
        try:
            validator_func(value)
        except Exception as e:  # ruff: ignore[blind-except] -- any failure becomes a validation message, not a crash
            return str(e)
        return True

    return validate


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
        validate=make_validator(validator_func),
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
    # questionary.select() has no `validate` hook (an already-listed choice needs no
    # per-keystroke validation), so a value-level validator is applied by re-asking on failure.
    validate = make_validator(validator_func)
    while True:
        question = questionary.select(
            message=prompt,
            choices=choices,
            default=default,
            instruction=help,
            **kwargs,
        )
        answer = question.ask()
        response = choices.get(answer, answer)
        result = validate(response)
        if result is True:
            return response
        questionary.print(str(result), style="fg:ansired")


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
