"""Tests for `project_forge.rendering.environment`."""

from pathlib import Path

import pytest
from jinja2 import Environment, TemplateNotFound
from jinja2.exceptions import UndefinedError

from project_forge.rendering.environment import InheritanceLoader, SuperUndefined
from project_forge.rendering.templates import InheritanceMap, ProcessMode, TemplateFile

RW_MODE = ProcessMode.render | ProcessMode.write


@pytest.fixture
def init_map(tmp_path: Path) -> InheritanceMap:
    """Create a simple template inheritance map."""
    p1 = tmp_path / "dir1" / "a.txt"
    p1.parent.mkdir(parents=True, exist_ok=True)
    p1.write_text("{% extends 'a.txt' %}")
    p2 = tmp_path / "dir2" / "a.txt"
    p2.parent.mkdir(parents=True, exist_ok=True)
    p2.write_text("{% extends 'a.txt' %}")
    p3 = tmp_path / "dir3" / "a.txt"
    p3.parent.mkdir(parents=True, exist_ok=True)
    p3.write_text("{% extends 'a.txt' %}")
    return InheritanceMap(
        {"a.txt": TemplateFile(p1, RW_MODE)},
        {"a.txt": TemplateFile(p2, RW_MODE)},
        {"a.txt": TemplateFile(p3, RW_MODE)},
    )


class TestInheritanceMap:
    """Tests for InheritanceMap."""

    def test_is_empty_returns_true_when_empty(self):
        """When an inheritance map is empty, is_empty returns true."""
        assert InheritanceMap().is_empty

    def test_is_empty_returns_false_when_not_empty(self, init_map: InheritanceMap):
        """When an inheritance map is not empty, is_empty returns false."""
        assert not init_map.is_empty

    def test_inheritance_for_key_returns_values_in_reverse_order(self, init_map: InheritanceMap):
        """When a key is provided, inheritance returns the values in reverse order."""
        assert init_map.inheritance("a.txt") == [
            init_map.maps[2]["a.txt"],
            init_map.maps[1]["a.txt"],
            init_map.maps[0]["a.txt"],
        ]

    def test_inheritance_for_missing_key_returns_empty_list(self, init_map: InheritanceMap):
        """The inheritance of a missing key returns empty list."""
        assert init_map.inheritance("b") == []


class TestSuperUndefined:
    """Tests for SuperUndefined."""

    def test_getattr_raises_undefined_error(self):
        """Accessing an arbitrary attribute raises an UndefinedError."""
        sup_undefined = SuperUndefined()
        with pytest.raises(UndefinedError):
            assert sup_undefined.__getattr__("valid_attr") == False

    def test_getattr_jinja_pass_arg_returns_false(self):
        """Accessing the `jinja_pass_arg` attribute returns False."""
        sup_undefined = SuperUndefined()
        assert sup_undefined.__getattr__("jinja_pass_arg") == False

    def test_getattr_dunder_attribute_raises_attribute_error(self):
        """Accessing a dunder attribute raises an AttributeError."""
        sup_undefined = SuperUndefined()
        with pytest.raises(AttributeError):
            sup_undefined.__getattr__("__dunder_attr__")

    def test_calling_an_instance_returns_empty_string(self):
        """Calling a SuperUndefined instance returns an empty string."""
        sup_undefined = SuperUndefined()
        assert sup_undefined.__call__() == ""


class TestInheritanceLoader:
    """Tests for InheritanceLoader."""

    def test_get_source_returns_inheritance_key(self, init_map: InheritanceMap):
        """"""
        # Prepare environments and data
        loader = InheritanceLoader(init_map)
        env = Environment(loader=loader)
        template_name = "a.txt"

        # Test when the get_source is provided with valid template name
        try:
            source, _, _ = env.loader.get_source(env, template_name)
            assert isinstance(source, str)
        except TemplateNotFound as e:
            pytest.fail(f"Unexpected TemplateNotFound error: {str(e)}")

    def test_get_source_for_missing_key_raises_error(self, init_map: InheritanceMap):
        # Test when the get_source is provided with invalid template name
        loader = InheritanceLoader(init_map)
        env = Environment(loader=loader)
        template_name = "invalid_template"

        with pytest.raises(TemplateNotFound):
            env.loader.get_source(env, "invalid_template")

    def test_get_source_beyond_inheritance_raises_error(self, init_map: InheritanceMap):
        """Test when the get_source is provided with a template number beyond the inheritance."""
        loader = InheritanceLoader(init_map)
        env = Environment(loader=loader)
        template_name = "a.txt"

        with pytest.raises(TemplateNotFound):
            env.loader.get_source(env, f"3/{template_name}")

    def test_get_source_for_last_template_removes_extends_tag(self, init_map: InheritanceMap):
        """Test when the get_source is provided with a template number one below the inheritance."""
        loader = InheritanceLoader(init_map)
        env = Environment(loader=loader)
        template_name = "a.txt"

        source = env.loader.get_source(env, f"2/{template_name}")
        assert source[0] == ""
