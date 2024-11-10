"""Test the merge_files.helpers functions."""

from collections import OrderedDict
from typing import Any

import pytest
from immutabledict import immutabledict
from pytest import param

from project_forge.context_builder import data_merge


@pytest.mark.parametrize(
    ["dict_list", "expected"],
    [
        param([{"a": 1}, {"a": 2}], {"a": 2}, id="dict 2 overwrites dict 1"),
        param([{"a": 1}, {"b": 2}], {"a": 1, "b": 2}, id="simple dict merge"),
        param(
            [{"a": {"b": 2}}, {"a": {"b": 3}}],
            {"a": {"b": 3}},
            id="nested dict 2 overwrites nested dict 1",
        ),
        param(
            [{"a": {"b": 1}}, {"a": {"c": 2}}],
            {"a": {"b": 1, "c": 2}},
            id="merge nested dicts",
        ),
    ],
)
def test_nested_overwrite(dict_list: list, expected: dict):
    """
    Make sure the deep merge is doing the right thing.
    """
    assert data_merge.nested_overwrite(*dict_list) == expected


@pytest.mark.parametrize(
    ["args", "expected"],
    [
        param([{"a": 1}, {"a": 2}], {"a": 2}, id="dict 2 scalars overwrites dict 1"),
        param([{"a": 1}, {"b": 2}], {"a": 1, "b": 2}, id="simple dict merge"),
        param(
            [{"a": {"b": 2}}, {"a": {"b": 3}}],
            {"a": {"b": 3}},
            id="nested dict 2 scalars overwrites nested dict 1 scalars",
        ),
        param(
            [{"a": {"b": 1}}, {"a": {"c": 2}}],
            {"a": {"b": 1, "c": 2}},
            id="merge nested dicts",
        ),
        param([[1, 2], [2, 3]], [1, 2, 3], id="merge lists"),
        param([(1, 2), (2, 3)], (1, 2, 3), id="merge tuples"),
        param([{1, 2}, {2, 3}], {1, 2, 3}, id="merge sets"),
        param(
            [{"a": [1]}, {"a": [2]}],
            {"a": [1, 2]},
            id="dict 2 iterable merges with dict 1 iterable",
        ),
        param([1, 2], 2, id="scalar 2 overwrites scalar 1"),
        param(
            [OrderedDict({"first": 1, "second": 2}), {"second": "two", "third": 3}],
            OrderedDict({"first": 1, "second": "two", "third": 3}),
            id="dict into ordered dict",
        ),
        param(
            [{"first": 1, "second": 2}, OrderedDict({"third": 3})],
            OrderedDict({"first": 1, "second": 2, "third": 3}),
            id="ordered dict into dict",
        ),
    ],
)
def test_comprehensive_merge(args: list, expected: Any):
    """
    Make sure the deep merge is doing the right thing.
    """
    assert data_merge.comprehensive_merge(*args) == expected


def test_comprehensive_merge_list_of_dicts():
    """A list of dicts should resolve into a list of immutabledicts in random order."""
    result = data_merge.comprehensive_merge([{"a": 1}, {"b": 2}], [{"c": 3}, {"d": 4}])
    expected = [
        immutabledict({"d": 4}),
        immutabledict({"c": 3}),
        immutabledict({"b": 2}),
        immutabledict({"a": 1}),
    ]
    assert isinstance(result, list)
    assert set(result) == set(expected)


class TestFreezeData:
    """Tests for the `freeze_data` function."""

    def test_scalars_return_scalars(self):
        """Scalar values are returned as is."""
        assert data_merge.freeze_data(None) is None
        assert data_merge.freeze_data("test") == "test"
        assert data_merge.freeze_data(123) == 123
        assert data_merge.freeze_data(3.14) == 3.14
        assert data_merge.freeze_data(b"binary") == b"binary"
        assert data_merge.freeze_data(True) is True

    def test_tuple_returns_tuple(self):
        """A tuple value returns a tuple."""
        result = data_merge.freeze_data((1, 2, 3))
        assert isinstance(result, tuple)
        assert result == (1, 2, 3)

    def test_tuple_containing_list_converts_to_tuple(self):
        """If a tuple contains a list, it is converted to a tuple."""
        result = data_merge.freeze_data((1, 2, [3, 4]))
        assert isinstance(result, tuple)
        assert len(result) == 3
        assert result[0] == 1
        assert result[1] == 2
        assert result[2] == (3, 4)

    def test_named_tuple_returns_namedtuple(self):
        """A named tuple returns a named tuple."""
        from collections import namedtuple

        Point = namedtuple("Point", ["x", "y"])
        point = Point(1, 2)
        result = data_merge.freeze_data(point)
        assert isinstance(result, Point)
        assert result.x == 1
        assert result.y == 2

    def test_list_converted_to_tuple(self):
        result = data_merge.freeze_data([1, 2, 3, 4])
        assert isinstance(result, tuple)
        assert result == (1, 2, 3, 4)

    def test_dict_converted_to_immutabledict(self):
        result = data_merge.freeze_data({"one": 1, "two": 2, "three": 3, "four": [4, 5]})
        assert isinstance(result, immutabledict)
        assert result["one"] == 1
        assert result["two"] == 2
        assert result["three"] == 3
        assert isinstance(result["four"], tuple)
        assert result["four"] == (4, 5)

    def test_ordered_dict_converted_to_immutabledict(self):
        """An `OrderedDict` is converted to an `immutabledict`."""
        ordered_dict = OrderedDict([("one", 1), ("two", 2), ("three", 3), ("four", [4, 5])])
        result = data_merge.freeze_data(ordered_dict)
        assert isinstance(result, immutabledict)
        assert result["one"] == 1
        assert result["two"] == 2
        assert result["three"] == 3
        assert isinstance(result["four"], tuple)
        assert result["four"] == (4, 5)

    def test_set_returns_frozenset(self):
        """A `set` is converted to a `frozenset`."""
        result = data_merge.freeze_data({1, 2, 3, 4})
        assert isinstance(result, frozenset)
        assert result == frozenset([1, 2, 3, 4])

    def test_non_supported_type_raises_error(self):
        """An unsupported raises an error."""
        with pytest.raises(ValueError):
            data_merge.freeze_data(object)


class TestUpdate:
    """Tests for the `update` function."""

    def test_default_behavior_is_update(self):
        """The default behavior for dicts is like `update`."""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"a": 3, "c": 4}
        assert data_merge.update(dict1, dict2) == {"a": 3, "b": 2, "c": 4}

    def test_all_empty_dicts_returns_empty_dict(self):
        dict1 = {}
        dict2 = {}
        assert data_merge.update(dict1, dict2) == {}

    @pytest.mark.parametrize(
        "updated_dict, updated_key, updated_value",
        [({"a": 1, "b": 2}, "a", 3), ({"a": 1, "b": 2}, "b", 4), ({"a": 1, "b": 2, "c": 3}, "c", 5)],
    )
    def test_overwrite_contains_key(self, updated_dict, updated_key, updated_value):
        dict_to_update = {updated_key: updated_value}
        expected_dict = {**updated_dict, **dict_to_update}
        assert data_merge.update(updated_dict, dict_to_update) == expected_dict
