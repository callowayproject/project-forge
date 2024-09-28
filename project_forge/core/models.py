"""Data models core to project forge."""

from typing import Any, Callable, Literal, Optional, Protocol, TypeVar, Union

T = TypeVar("T")


class UndefinedType:
    """A singleton that indicates an undefined state."""

    def __repr__(self) -> str:
        return "Undefined"

    def __copy__(self: T) -> T:
        return self

    def __reduce__(self) -> str:
        return "Undefined"

    def __deepcopy__(self: T, _: Any) -> T:
        return self


Undefined = UndefinedType()
Skipped = Undefined

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
Must start with a letter and can contain alpha-numeric and underscores."""


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

        Returns:
            The answer to the prompt.
        """
        ...
