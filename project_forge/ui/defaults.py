"""A UI that will return the defaults."""

from typing import Any, Callable, Optional

from project_forge.core.types import QUESTION_TYPE_CAST, QuestionType


def return_defaults(
    prompt: str,
    type: QuestionType = "str",
    help: Optional[str] = None,
    choices: Optional[dict] = None,
    default: Any = None,
    multiselect: bool = False,
    validator_func: Optional[Callable] = None,
    **kwargs,
) -> Any:
    """Return the default value."""
    cast_func = QUESTION_TYPE_CAST.get(type, lambda x: x)  # pragma: no-coverage
    return cast_func(default) if default is not None else ""
