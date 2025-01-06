"""Tests for the `rendering.expressions` module."""

import pytest
from pytest import param

from project_forge.rendering.expressions import render_bool_expression


class TestRenderBoolExpression:
    """Tests for the `render_bool_expression` function."""

    def test_any_non_false_string_is_true(self):
        """Any non-false string is True."""
        result = render_bool_expression("{% if True %}True{% endif %}")
        assert result is True

    @pytest.mark.parametrize(
        ["value"],
        [
            param("False", id="False"),
            param("false", id="false"),
            param("0", id="0"),
            param("", id="empty string"),
        ],
    )
    def test_render_string_false_as_boolean(self, value: str):
        result = render_bool_expression(f"{{% if False %}}{value}{{% endif %}}")
        assert result == False

    @pytest.mark.parametrize(
        ["value", "expected"],
        [
            param(True, True, id="True"),
            param(False, False, id="False"),
        ],
    )
    def test_boolean_returns_itself(self, value: bool, expected: bool):
        result = render_bool_expression(value)
        assert result == expected

    @pytest.mark.parametrize(["value", "expected"], [param(1, True, id="1"), param(0, False, id="0")])
    def test_context_based_rendering(self, value: int, expected: bool):
        result = render_bool_expression(
            "{% if context_value == 1 %}True{% else %}False{% endif %}", context={"context_value": value}
        )
        assert result == expected

    def test_string_condition_is_evaluated(self):
        """A string that doesn't start with `{` is wrapped in a template string."""
        result = render_bool_expression("key1 == 'value1'", context={"key1": "value1"})
        assert result is True
        result = render_bool_expression("key1 == 'value1'", context={"key1": "value2"})
        assert result is False
