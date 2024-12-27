"""Answer validators."""

from typing import Any, TypeVar

from project_forge.rendering.expressions import render_expression

T = TypeVar("T")


class ExprValidator:
    """A callable that will validate input by rendering an expression."""

    def __init__(self, expr: str = ""):
        self._expr = expr

    def __call__(self, value: T) -> T:
        """
        Validate the input.

        Args:
            value: The value to validate.

        Returns:
            The value if the expression returns nothing.

        Raises:
            ValueError: If the expression returns a value. The message of the ValueError is the rendered expression.
        """
        if result := render_expression(self._expr, {"value": value}):
            raise ValueError(result)
        return value


def is_int(value: Any) -> bool:
    """Is the value an int or convertible to an int?"""
    if not isinstance(value, (int, float, str, bool)):
        return False

    try:
        _ = int(value)
        return True
    except ValueError:
        return False


def is_float(value: Any) -> bool:
    """Is the value a float or convertible to a float?"""
    if not isinstance(value, (int, float, str, bool)):
        return False

    try:
        _ = float(value)
        return True
    except ValueError:
        return False


def is_bool(value: Any) -> bool:
    """Is the value a boolean or convertible to a boolean?"""
    if not isinstance(value, (int, float, str, bool)):
        return False

    try:
        _ = bool(value)
        return True
    except ValueError:
        return False
