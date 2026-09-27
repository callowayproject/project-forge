from typing import Any

import pytest
from prompt_toolkit.document import Document
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput
from prompt_toolkit.validation import ValidationError
from pytest import param
from questionary.prompts.common import build_validator

from project_forge.ui import terminal


@pytest.fixture(scope="function")
def input_pipe():
    """An input pipe for prompt Toolkit."""
    with create_pipe_input() as inp:
        yield inp


class KeyInputs:
    DOWN = "\x1b[B"
    UP = "\x1b[A"
    LEFT = "\x1b[D"
    RIGHT = "\x1b[C"
    ENTER = "\r"
    ESCAPE = "\x1b"
    CONTROLC = "\x03"
    CONTROLN = "\x0e"
    CONTROLP = "\x10"
    BACK = "\x7f"
    SPACE = " "
    TAB = "\x09"


class TestMakeValidator:
    """Tests for the make_validator function."""

    def test_none_validator_func_always_returns_true(self):
        """When there is no validator function, the resulting validator accepts anything."""
        validate = terminal.make_validator(None)
        assert validate("anything") is True

    def test_valid_input_returns_true(self):
        """When the validator function does not raise, the value is valid."""
        validate = terminal.make_validator(lambda value: value)
        assert validate("ok") is True

    def test_invalid_input_returns_error_message(self):
        """When the validator function raises ValueError, its message is returned."""

        def validator_func(value):
            raise ValueError("nope")

        validate = terminal.make_validator(validator_func)
        assert validate("bad") == "nope"


class TestAskQuestion:
    """Tests for the ask_question function."""

    @pytest.mark.parametrize(
        ["input_type", "input_str", "expected"],
        [
            param("str", "testing", "testing", id="str"),
            param("int", "1", 1, id="int"),
            param("float", "1.0", 1.0, id="float"),
        ],
    )
    def test_scalar_type_returns_correct_type(self, input_pipe, input_type: str, input_str: str, expected: Any):
        """Scalar question types will return the answer in the correct type."""
        input_pipe.send_text(f"{input_str}{KeyInputs.ENTER}")
        response = terminal.ask_question(
            "What is the answer?", type=input_type, input=input_pipe, output=DummyOutput()
        )
        assert response == expected

    @pytest.mark.parametrize(
        ["input_type", "default", "expected"],
        [
            param("str", "testing", "testing", id="str"),
            param("int", 1, 1, id="int"),
            param("float", 1.0, 1.0, id="float"),
        ],
    )
    def test_scalar_type_with_default_returns_default(self, input_pipe, input_type: str, default: Any, expected: Any):
        """Scalar question types with a default returns the default if only the enter key is pressed."""

        input_pipe.send_text(KeyInputs.ENTER)
        response = terminal.ask_question(
            "What are you doing?", type=input_type, default=default, input=input_pipe, output=DummyOutput()
        )
        assert response == expected

    def test_bool_type_returns_bool(self, input_pipe):
        """A `bool` type question returns a boolean."""

        input_pipe.send_text("y")
        response = terminal.ask_question("Question?", "bool", input=input_pipe, output=DummyOutput())
        assert response is True
        input_pipe.send_text("n")
        response = terminal.ask_question("Question?", "bool", input=input_pipe, output=DummyOutput())
        assert response is False

    def test_bool_type_with_default_returns_default(self, input_pipe):
        """A `bool` type question with a default returns the default if only the enter key is pressed."""

        input_pipe.send_text(KeyInputs.ENTER)
        response = terminal.ask_question("Question?", "bool", default=True, input=input_pipe, output=DummyOutput())
        assert response is True
        input_pipe.send_text(KeyInputs.ENTER)
        response = terminal.ask_question("Question?", "bool", default=False, input=input_pipe, output=DummyOutput())
        assert response is False

    @pytest.mark.parametrize(
        ["input_type", "choices", "expected"],
        [
            param("str", {"one": "one", "two": "two", "three": "three"}, ["two", "three"], id="str"),
            param("int", {"1": 1, "2": 2, "3": 3}, [2, 3], id="int"),
            param("float", {"1.0": 1.0, "2.0": 2.0, "3.0": 3.0}, [2.0, 3.0], id="float"),
        ],
    )
    def test_scalar_multiselect_returns_correct_type(self, input_pipe, input_type: str, choices: dict, expected: list):
        """Scalar question types will return the answer in the correct type."""

        input_pipe.send_text(KeyInputs.DOWN + KeyInputs.SPACE + KeyInputs.DOWN + KeyInputs.SPACE + KeyInputs.ENTER)
        response = terminal.ask_question(
            "What is the answer?",
            type=input_type,
            choices=choices,
            multiselect=True,
            input=input_pipe,
            output=DummyOutput(),
        )
        assert response == expected

    @pytest.mark.parametrize(
        ["input_type", "choices", "expected"],
        [
            param("str", {"one": "one", "two": "two", "three": "three"}, "two", id="str"),
            param("int", {"1": 1, "2": 2, "3": 3}, 2, id="int"),
            param("float", {"1.0": 1.0, "2.0": 2.0, "3.0": 3.0}, 2.0, id="float"),
        ],
    )
    def test_scalar_select_returns_correct_type(self, input_pipe, input_type: str, choices: dict, expected: Any):
        """Scalar question types will return the answer in the correct type."""

        input_pipe.send_text(KeyInputs.DOWN + KeyInputs.ENTER)
        response = terminal.ask_question(
            "What is the answer?",
            type=input_type,
            choices=choices,
            input=input_pipe,
            output=DummyOutput(),
        )
        assert response == expected

    def test_select_reprompts_when_validator_rejects_first_choice(self, input_pipe):
        """ask_question with choices re-prompts if the validator rejects the chosen value."""

        def validator_func(value):
            if value == "two":
                raise ValueError("two is not allowed")
            return value

        # first attempt selects "two" (rejected), second attempt selects "three"
        input_pipe.send_text(KeyInputs.DOWN + KeyInputs.ENTER + KeyInputs.DOWN + KeyInputs.DOWN + KeyInputs.ENTER)
        response = terminal.ask_question(
            "What is the answer?",
            choices={"one": "one", "two": "two", "three": "three"},
            validator_func=validator_func,
            input=input_pipe,
            output=DummyOutput(),
        )
        assert response == "three"

    def test_invalid_input_is_rejected_by_the_questionary_validator(self):
        """A validator_func that raises ValueError rejects bad input at the real questionary prompt."""

        def validator_func(value):
            if value != "valid":
                raise ValueError("must be 'valid'")
            return value

        validator = build_validator(terminal.make_validator(validator_func))

        with pytest.raises(ValidationError):
            validator.validate(Document("bad"))

        validator.validate(Document("valid"))  # does not raise

    def test_secret_returns_a_string(self, input_pipe):
        """The secret type should return a string."""
        input_pipe.send_text(f"secret{KeyInputs.ENTER}")
        response = terminal.ask_question(
            "What is the answer?",
            type="secret",
            input=input_pipe,
            output=DummyOutput(),
        )
        assert response == "secret"
