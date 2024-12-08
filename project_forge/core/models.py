"""Data models core to project forge."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Literal, Optional, Protocol, Union

TemplateEngine = Literal["default"]
"""Supported template engines."""

QuestionType = Literal["int", "float", "bool", "str", "multiline", "secret", "yaml", "json"]
"""Possible question types."""

QUESTION_TYPE_CAST = {
    "int": int,
    "float": float,
    "bool": bool,
    "str": str,
    "multiline": str,
    "secret": str,
    "yaml": str,
    "json": str,
}

ScalarType = Union[str, int, float, bool, None]

VARIABLE_REGEX = r"[a-zA-Z_][\w_]*"
"""The regular expression to validate a variable name.
Must start with a letter and can contain alphanumeric and underscores."""


@dataclass
class BuildResult:
    """The result of a build operation."""

    root_path: Path
    """The path to the rendered project."""

    context: dict[str, Any]
    """The rendered context for the project."""


class UIFunction(Protocol):
    """The function signature for a UI prompt."""

    def __call__(
        self,
        prompt: str,
        type: QuestionType = "str",
        help: Optional[str] = None,
        choices: Optional[dict] = None,
        default: Any = None,
        multiselect: bool = False,
        validator_func: Optional[Callable] = None,
        **kwargs: Any,
    ) -> Any:
        """
        A function that asks the user for input.

        Args:
            prompt: The prompt displayed to the user.
            type: The type of the answer
            help: Optional instructions for the user.
            choices: An optional dictionary of choices
            default: The default value.
            multiselect: Can the user select multiple answers?
            validator_func: A callable that takes an answer and returns True if it is valid.
            **kwargs: Additional keyword arguments to pass to the UI function.

        Returns:
            The answer to the prompt.
        """
        ...
