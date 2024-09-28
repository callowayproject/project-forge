import pytest
from project_forge.core.validators import is_int, is_float, is_bool
from pytest import param


class TestIsInt:
    @pytest.mark.parametrize(
        "value",
        [
            param(121, id="integer"),
            param("233", id="string"),
            param(0, id="zero"),
            param(-17, id="negative"),
            param("-56", id="negative string"),
            param(3.14, id="float"),
        ],
    )
    def test_positive_scenarios(self, value):
        assert is_int(value) == True

    @pytest.mark.parametrize(
        "value",
        [
            param("abc", id="string"),
            param(None, id="none"),
            param([1, 2], id="list"),
            param((1, 2), id="tuple"),
            param({1: "one", 2: "two"}, id="dict"),
        ],
    )
    def test_negative_scenarios(self, value):
        assert is_int(value) == False


class TestIsFloat:
    @pytest.mark.parametrize(
        "value",
        [
            param(3.14, id="float"),
            param(-3.14, id="negative float"),
            param(0.0, id="zero float"),
            param(-0.0, id="negative zero float"),
            param("2.71828", id="string float"),
            param("-2.71828", id="negative string float"),
            param(10, id="integer"),
        ],
    )
    def test_positive_scenarios(self, value):
        assert is_float(value) is True

    @pytest.mark.parametrize(
        "value",
        [
            param("abc", id="string"),
            param(None, id="none"),
            param([1, 2], id="list"),
            param((1, 2), id="tuple"),
            param({1: "one", 2: "two"}, id="dict"),
        ],
    )
    def test_negative_scenarios(self, value):
        assert is_float(value) is False


class TestIsBool:
    @pytest.mark.parametrize(
        "value",
        [
            param(True, id="True"),
            param(False, id="False"),
            param(0, id="0"),
            param(1, id="1"),
            param("True", id="string True"),
            param("False", id="string False"),
            param("true", id="string true"),
            param("false", id="string false"),
            param("abc", id="any string"),
            param(3.14, id="any float"),
            param(145, id="any integer"),
        ],
    )
    def test_positive_scenarios(self, value):
        assert is_bool(value)

    @pytest.mark.parametrize(
        "value",
        [
            param(None, id="none"),
            param([1, 2], id="list"),
            param((1, 2), id="tuple"),
            param({1: "one", 2: "two"}, id="dict"),
        ],
    )
    def test_negative_scenarios(self, value):
        assert is_bool(value) is False
