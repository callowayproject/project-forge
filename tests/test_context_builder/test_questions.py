"""Tests for project_forge.context_builder.questions.py."""

from unittest.mock import MagicMock

import pytest

from project_forge.context_builder.questions import Choice, answer_question, filter_choices
from project_forge.models.pattern import Question


@pytest.fixture
def running_context():
    return {"key1": "value1", "key2": "value2"}


@pytest.fixture
def choices(running_context):
    choice1 = Choice(label="label1", value="value1", skip_when="{% if key1 == 'value1' %}True{% endif %}")
    choice2 = Choice(label="label2", value="value2", skip_when="{% if key2 == 'value3' %}True{% endif %}")
    choice3 = Choice(label="label3", value="value3")
    return [choice1, choice2, choice3]


@pytest.fixture(scope="function")
def question():
    return Question(
        name="Test",
        prompt="Test prompt?",
        type="str",
        help="This is a test question",
        choices=[],
        default="Local Default",
    )


@pytest.fixture
def answer_map():
    return {"Test": "Answer"}


@pytest.fixture
def default_overrides():
    return {"Test": "Overridden Default"}


class TestFilterChoices:
    """Tests for the `filter_choices` function."""

    def test_ignores_skipped(self, choices, running_context):
        """Choices with a valid `skip_when` attribute should be skipped."""
        filtered_choices = filter_choices(choices, running_context)
        assert "label1" not in filtered_choices

    def test_includes_non_skipped(self, choices, running_context):
        filtered_choices = filter_choices(choices, running_context)
        assert "label2" in filtered_choices

    # def test_filter_choices_correct_values(self, choices, running_context):
    #     filtered_choices = filter_choices(choices, running_context)
    #     assert filtered_choices["label2"] == "value2"

    def test_choices_empty_when_all_skipped(self):
        choices = [Choice(label="label1", value="value1", skip_when="True")]
        filtered_choices = filter_choices(choices, {})
        assert not filtered_choices


class TestAnswerQuestion:
    """Tests for the `answer_question` function."""

    def test_when_question_exists_in_answer_map_it_is_used(self, question, running_context, answer_map):
        mock_ui = MagicMock()
        result = answer_question(question, running_context, mock_ui, answer_map)
        assert result == {"Test": "Answer"}
        assert mock_ui.call_count == 0

    def test_when_question_exists_in_running_context_it_is_used(self, question, running_context):
        question.name = "key1"
        mock_ui = MagicMock(return_value="Not Correct")
        result = answer_question(question, running_context, mock_ui)
        assert result == {"key1": running_context["key1"]}

    def test_default_overrides_is_used(self, question, running_context, default_overrides):
        question.default = "Local Default"
        mock_ui = MagicMock(return_value=default_overrides[question.name])
        result = answer_question(question, running_context, mock_ui, default_overrides=default_overrides)
        assert result == {"Test": default_overrides[question.name]}

    def test_default_is_used(self, question, running_context):
        mock_ui = MagicMock(return_value="Local Default")
        result = answer_question(question, running_context, mock_ui)
        assert result == {"Test": "Local Default"}

    def test_default_used_if_force_default_true(self, question, running_context):
        mock_ui = MagicMock(return_value="Not Default")
        question.force_default = "True"
        result = answer_question(question, running_context, mock_ui)
        assert result == {"Test": "Local Default"}
        assert mock_ui.call_count == 0

    def test_return_dict(self, question, running_context):
        mock_ui = MagicMock(return_value="My Answer")
        result = answer_question(question, running_context, mock_ui)
        assert mock_ui.call_count == 1
        assert result == {"Test": "My Answer"}
