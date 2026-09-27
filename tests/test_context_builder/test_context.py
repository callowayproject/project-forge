"""Tests for the project_forge.context_builder.context module."""

import datetime
from unittest.mock import MagicMock, Mock, patch

from project_forge.context_builder.context import build_context, get_starting_context, update_context
from project_forge.models.composition import Composition
from project_forge.models.overlay import Overlay
from project_forge.models.pattern import Pattern
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
            patch("project_forge.context_builder.context.execute_task") as mock_execute_task,
        ):
            composition = self.create_mock_composition(
                extra_context={
                    "key": "{{ value }}",
                    "overlay_key": "I should get overwritten",
                }
            )

            self.set_mocked_return_values(
                mock_get_starting_context, mock_render_expression, mock_process_overlay, mock_execute_task
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
                mock_execute_task,
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

    def test_initial_context_merges_with_extra_context(self):
        """When an initial context is passed, it merges with the extra context."""
        ui = Mock()

        with (
            patch("project_forge.context_builder.context.get_starting_context") as mock_get_starting_context,
            patch("project_forge.context_builder.context.render_expression") as mock_render_expression,
            patch("project_forge.context_builder.context.process_overlay") as mock_process_overlay,
            patch("project_forge.context_builder.context.execute_task") as mock_execute_task,
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
                mock_execute_task,
            )
            context = build_context(composition, ui, initial_context)

            assert context == {
                "key": "rendered_value",
                "overlay_key": "overlay_value",
                "initial_key": "rendered_value",
            }

            self.assert_mocked_functions_called(
                mock_render_expression,
                mock_process_overlay,
                mock_get_starting_context,
                mock_execute_task,
            )

    def test_interleaved_steps_apply_mixed_case_merge_key_strategy(self, tmp_path):
        """A mixed-case merge key must use its configured strategy, not fall back to comprehensive merge.

        Two overlays (not composition.extra_context, which stringifies values via render_expression) are used
        so `myKey` stays a real list on both sides of the conflicting merge, with a real Task interleaved
        between them.
        """
        # Assemble
        template_dir = tmp_path / "templates"
        template_dir.mkdir()
        pattern_file1 = tmp_path / "pattern1.yaml"
        pattern_file1.write_text("")
        pattern_file2 = tmp_path / "pattern2.yaml"
        pattern_file2.write_text("")

        overlay1 = Overlay(pattern_location=str(pattern_file1))
        overlay1._pattern = Pattern(template_location=str(template_dir), extra_context={"myKey": [1, 2, 3]})

        task = Task(command=["echo", "ok"], context_variable_name="task_output")

        overlay2 = Overlay(pattern_location=str(pattern_file2))
        overlay2._pattern = Pattern(template_location=str(template_dir), extra_context={"myKey": [4, 5, 6]})

        composition = Composition(
            steps=[overlay1, task, overlay2],
            merge_keys={"myKey": "update"},
        )

        # Act
        context = build_context(composition, ui=Mock())

        # Assert: "update" replaces the list instead of comprehensive's concatenation.
        assert context["myKey"] == [4, 5, 6]
        assert context["task_output"] == "ok"

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
        self, mock_get_starting_context, mock_render_expression, mock_process_overlay, mock_execute_task
    ):
        """Set the return values for the mocked functions."""
        mock_get_starting_context.return_value = {}
        mock_render_expression.return_value = "rendered_value"
        mock_process_overlay.return_value = {"overlay_key": "overlay_value"}
        mock_execute_task.return_value = {}

    def assert_mocked_functions_called(
        self, mock_render_expression, mock_process_overlay, mock_get_starting_context, mock_execute_task
    ):
        """Assert that the mocked functions were called."""
        assert mock_render_expression.called
        assert mock_process_overlay.called
        assert mock_get_starting_context.called
        assert mock_execute_task.called


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
