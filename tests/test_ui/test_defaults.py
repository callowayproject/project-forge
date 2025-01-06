"""Tests for ui.defaults."""

from unittest.mock import Mock

from project_forge.core.types import QUESTION_TYPE_CAST
from project_forge.ui.defaults import return_defaults


class TestReturnDefaults:
    """Tests for the return_defaults function."""

    def test_returns_default_value_as_is(self):
        """Test that return_defaults returns the provided default value."""
        default_value = "test_value"
        result = return_defaults(prompt="Test prompt", default=default_value, type="str")
        assert result == default_value

    def test_converts_default_value_with_cast_function(self, monkeypatch):
        """Test that the return_defaults function applies the cast function."""
        mock_cast_func = Mock(return_value="casted_value")
        monkeypatch.setitem(QUESTION_TYPE_CAST, "str", mock_cast_func)

        result = return_defaults(prompt="Test prompt", default="value_to_cast", type="str")
        mock_cast_func.assert_called_once_with("value_to_cast")
        assert result == "casted_value"

    def test_returns_empty_string_if_default_is_none(self):
        """Test that return_defaults returns an empty string if default is None."""
        result = return_defaults(prompt="Test prompt", default=None, type="str")
        assert result == ""

    def test_handles_missing_cast_function_gracefully(self):
        """Test that return_defaults gracefully handles missing cast functions."""
        result = return_defaults(prompt="Test prompt", default="test_value", type="unknown_type")
        assert result == "test_value"

    def test_supports_kwargs_passthrough(self):
        """Ensure **kwargs can be accepted without breaking functionality."""
        result = return_defaults(
            prompt="Test prompt",
            default="test_value",
            custom_kwarg="custom_value",
        )
        assert result == "test_value"
