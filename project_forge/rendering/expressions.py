"""Render template expressions."""

from typing import MutableMapping, Optional, Union

from project_forge.rendering.environment import load_environment


def render_bool_expression(expression: Union[str, bool], context: Optional[MutableMapping] = None) -> bool:
    """
    Render a template expression and convert the result to a boolean.

    Any string expression that is not a template string is wrapped in an `{% if ... %}` block.

    Args:
        expression: A string expression, a template string, or a boolean.
        context: The context used to render a string

    Returns:
        True if the boolean is True, or the rendered result is not one of `False`, `false`, `0`, an empty string.
    """
    if isinstance(expression, bool):
        return expression
    elif not expression.startswith("{"):
        expression = f"{{% if {expression} %}}True{{% else %}}False{{% endif %}}"

    result = render_expression(expression, context)
    return result not in {"False", "false", "0", ""}


def render_expression(expression: str, context: Optional[MutableMapping] = None) -> str:
    """Render a template expression."""
    context = context or {}
    env = load_environment()
    template = env.from_string(str(expression))
    return template.render(**context).strip()
