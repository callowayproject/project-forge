from typing import Any

import pytest
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput
from pytest import param

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
