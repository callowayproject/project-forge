"""Tests for the project_forge.context_builder.overlays module."""

from pathlib import Path

from project_forge.context_builder.overlays import merge_contexts, process_overlay
from project_forge.models.overlay import Overlay
from project_forge.ui.defaults import return_defaults

# composition_path is None
# composition_path is File
# mock read_pattern_file to return a pattern
# mock_ui and mock_answer_question
# result context is the combination of the extra contexts, the initial context, and the answers to all the questions


class TestProcessOverlay:
    """Tests for the `process_overlay` function."""

    def test_uses_running_context_defaults(self, fixtures_dir: Path):
        """It uses the running context for the defaults if none are provided."""
        overlay = Overlay.model_validate(
            {"pattern_location": "python-package/pattern.toml"},
            context={"composition_path": fixtures_dir.joinpath("composition1.toml")},
        )
        running_context = {
            "project_name": "test-project",
            "package_name": "test_package",
            "package_path": "test-repo/test_package",
            "repo_name": "test-repo",
            "project_description": "A description",
            "initial_version": "0.1.0",
            "author": "Testy McTestface",
        }
        result = process_overlay(overlay, running_context, return_defaults)
        assert result == running_context

    def test_uses_answers_from_ui(self, fixtures_dir: Path):
        """It uses the UI answers to update the running context."""
        overlay = Overlay.model_validate(
            {"pattern_location": "python-package/pattern.toml"},
            context={"composition_path": fixtures_dir.joinpath("composition1.toml")},
        )
        running_context = {}
        answers = {
            "project_name": "my-project",
            "package_name": "my_package",
            "repo_name": "my-repo",
            "project_description": "Is this thing on?",
            "initial_version": "1.0.0",
            "author": "Boaty McBoatface",
        }
        expected_result = {**answers, "package_path": "my-repo/my_package"}
        answers_iter = iter(answers.values())

        def mock_ui(*args, **kwargs):
            return next(answers_iter)

        result = process_overlay(overlay, running_context, mock_ui)
        assert result == expected_result


class TestMergeContexts:
    """Tests for the `merge_contexts` function."""

    def test_overlay_context_overrides_all_contexts(self):
        """The override context will always override everything."""
        initial_context = {"foo": "initial"}
        pattern_context = {"foo": "pattern", "bar": "pattern"}
        overlay_context = {"foo": "overlay"}

        expected_result = {"foo": "overlay", "bar": "pattern"}
        assert merge_contexts(initial_context, overlay_context, pattern_context) == expected_result

    def test_pattern_context_overrides_initial_context(self):
        """The pattern context will always override the initial context."""
        initial_context = {"foo": "initial", "bar": "initial"}
        pattern_context = {"foo": "pattern", "bar": "pattern"}
        overlay_context = {"foo": "overlay"}

        expected_result = {"foo": "overlay", "bar": "pattern"}
        assert merge_contexts(initial_context, overlay_context, pattern_context) == expected_result

    def test_overlay_context_may_be_empty(self):
        """The override context can be empty."""
        initial_context = {"foo": "initial"}
        pattern_context = {"foo": "pattern", "bar": "pattern"}
        overlay_context = {}

        expected_result = {"foo": "pattern", "bar": "pattern"}
        assert merge_contexts(initial_context, overlay_context, pattern_context) == expected_result

    def test_pattern_context_may_be_empty(self):
        """The pattern context may be empty."""
        initial_context = {"foo": "initial"}
        pattern_context = {}
        overlay_context = {"foo": "overlay"}

        expected_result = {"foo": "overlay"}
        assert merge_contexts(initial_context, overlay_context, pattern_context) == expected_result

    def test_all_contexts_may_be_empty(self):
        """All the contexts may be empty."""
        initial_context = {}
        pattern_context = {}
        overlay_context = {}

        assert merge_contexts(initial_context, overlay_context, pattern_context) == {}

    def test_values_are_rendered(self):
        """Values for the contexts are rendered using Jinja2."""
        initial_context = {"foo": "initial", "bar": "initial"}
        pattern_context = {"foo": "pattern"}
        overlay_context = {"foo": "{{ bar }}"}

        expected_result = {"foo": "initial", "bar": "initial"}
        assert merge_contexts(initial_context, overlay_context, pattern_context) == expected_result
