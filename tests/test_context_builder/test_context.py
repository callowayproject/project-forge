"""Tests for the project_forge.context_builder.context module."""

import datetime
from unittest.mock import MagicMock, Mock, patch

from project_forge.context_builder.context import build_context, get_starting_context, update_context
from project_forge.models.composition import Composition
from project_forge.models.overlay import Overlay
from project_forge.models.task import Task


def test_get_starting_context_contains_correct_keys():
    """The starting context contains all the expected keys."""
    context = get_starting_context()
    assert isinstance(context, dict)
    assert "now" in context
    assert isinstance(context["now"], datetime.datetime)
    assert context["now"].tzinfo == datetime.timezone.utc


class TestBuildContext:
    """Tests for the build_context function."""

    def test_extra_context_and_overlays_composes_correctly(self):
        """Build context should render extra contexts and merge overlay contexts."""
        ui = Mock()

        with (
            patch("project_forge.context_builder.context.get_starting_context") as mock_get_starting_context,
            patch("project_forge.context_builder.context.render_expression") as mock_render_expression,
            patch("project_forge.context_builder.context.process_overlay") as mock_process_overlay,
            patch("project_forge.context_builder.context.process_task") as mock_process_task,
        ):
            composition = self.create_mock_composition(
                extra_context={
                    "key": "{{ value }}",
                    "overlay_key": "I should get overwritten",
                }
            )

            self.set_mocked_return_values(
                mock_get_starting_context, mock_render_expression, mock_process_overlay, mock_process_task
            )
            context = build_context(composition, ui)

            assert context == {
                "key": "rendered_value",
                "overlay_key": "overlay_value",
            }

            self.assert_mocked_functions_called(
                mock_render_expression,
                mock_process_overlay,
                mock_get_starting_context,
                mock_process_task,
            )

    def test_empty_composition_is_starting_context(self):
        """Building a context with an empty composition returns the starting context."""
        ui = Mock()
        starting_context = {"key": "value"}
        with (
            patch("project_forge.context_builder.context.get_starting_context") as mock_get_starting_context,
            patch("project_forge.context_builder.context.render_expression") as mock_render_expression,
            patch("project_forge.context_builder.context.process_overlay") as mock_process_overlay,
        ):
            composition = self.create_mock_composition()
            composition.steps = []

            mock_get_starting_context.return_value = starting_context
            mock_render_expression.return_value = ""
            mock_process_overlay.return_value = {}

            context = build_context(composition, ui)

            assert context == starting_context
            mock_render_expression.assert_not_called()
            mock_process_overlay.assert_not_called()
            assert mock_get_starting_context.called

    def initial_context_merges_with_extra_context(self):
        """When an initial context is passed, it merges with the extra context."""
        ui = Mock()

        with (
            patch("project_forge.context_builder.context.get_starting_context") as mock_get_starting_context,
            patch("project_forge.context_builder.context.render_expression") as mock_render_expression,
            patch("project_forge.context_builder.context.process_overlay") as mock_process_overlay,
            patch("project_forge.context_builder.context.process_task") as mock_process_task,
        ):
            composition = self.create_mock_composition(
                extra_context={
                    "key": "{{ value }}",
                    "overlay_key": "I should get overwritten",
                }
            )
            initial_context = {"initial_key": "initial_value"}

            self.set_mocked_return_values(
                mock_get_starting_context,
                mock_render_expression,
                mock_process_overlay,
                mock_process_task,
            )
            context = build_context(composition, ui, initial_context)

            assert context == {
                "key": "rendered_value",
                "overlay_key": "overlay_value",
                "initial_key": "initial_value",
            }

            self.assert_mocked_functions_called(
                mock_render_expression,
                mock_process_overlay,
                mock_get_starting_context,
                mock_process_task,
            )

    def create_mock_composition(self, extra_context=None):
        """Create a mock composition."""
        result = MagicMock(spec=Composition)
        result.merge_keys = {}
        result.extra_context = extra_context or {}
        result.steps = [
            MagicMock(spec=Overlay),
            MagicMock(spec=Task),
            MagicMock(spec=Overlay),
            MagicMock(spec=Task),
        ]
        return result

    def set_mocked_return_values(
        self, mock_get_starting_context, mock_render_expression, mock_process_overlay, mock_process_task
    ):
        """Set the return values for the mocked functions."""
        mock_get_starting_context.return_value = {}
        mock_render_expression.return_value = "rendered_value"
        mock_process_overlay.return_value = {"overlay_key": "overlay_value"}
        mock_process_task.return_value = {}

    def assert_mocked_functions_called(
        self, mock_render_expression, mock_process_overlay, mock_get_starting_context, mock_process_task
    ):
        """Assert that the mocked functions were called."""
        assert mock_render_expression.called
        assert mock_process_overlay.called
        assert mock_get_starting_context.called
        assert mock_process_task.called


class TestUpdateContext:
    """Tests for the update_context function."""

    def test_default_behavior_uses_comprehensive_merge(self):
        """The result should contain all the keys and the values should be merged comprehensively."""
        # Assemble
        merge_keys = {}
        left = {"a": 1, "b": [1, 2, 3], "c": 3}
        right = {"a": 2, "b": [4, 5, 6], "d": 4}
        expected_result = {"a": 2, "b": [1, 2, 3, 4, 5, 6], "c": 3, "d": 4}

        # Act
        result = update_context(merge_keys, left, right)

        # Assert
        assert result == expected_result, f"Expected {expected_result}, but got {result}"

    def test_updating_empty_dicts_returns_empty_dict(self):
        """Updating an empty dict with an empty dict should return an empty dict."""
        # Assemble
        merge_keys = {"a": "update", "b": "nested_overwrite"}
        left = {}
        right = {}
        expected_result = {}

        # Act
        result = update_context(merge_keys, left, right)

        # Assert
        assert result == expected_result, f"Expected {expected_result}, but got {result}"

    def test_respects_methods_in_merge_keys(self):
        """Update context should use the specified merge strategy."""
        # Assemble
        merge_keys = {"b": "update"}
        left = {"a": 1, "b": [1, 2, 3], "c": 3}
        right = {"a": 2, "b": [4, 5, 6], "d": 4}
        expected_result = {"a": 2, "b": [4, 5, 6], "c": 3, "d": 4}

        # Act
        result = update_context(merge_keys, left, right)

        # Assert
        assert result == expected_result, f"Expected {expected_result}, but got {result}"
