"""Tests for project_forge.rendering.templates."""

from pathlib import Path

from project_forge.rendering import templates
import pytest
from project_forge.rendering.templates import catalog_templates, catalog_inheritance, InheritanceMap
from icecream import ic


def generate_fake_templates(location: Path):
    """Create a directory of dummy templates."""
    template1_dir = location / "template1"
    template1_dir.mkdir(parents=True, exist_ok=True)
    subdir = template1_dir / "subdir"
    subdir.mkdir()
    empty_dir = template1_dir / "empty"
    empty_dir.mkdir()
    template2_dir = location / "template2"
    template2_dir.mkdir(parents=True, exist_ok=True)

    (template1_dir / "inherit.txt").touch()
    (template2_dir / "inherit.txt").touch()
    (template1_dir / "template1.txt").touch()
    (template2_dir / "template2.txt").touch()
    (subdir / "subdir.txt").touch()


class TestCatalogTemplates:
    """Tests of the `catalog_templates` function."""

    def test_result_keys_are_relative_filepaths(self, tmp_path: Path):
        """The returned keys are relative filepaths as strings."""
        # Assemble
        generate_fake_templates(tmp_path)
        template1 = tmp_path / "template1"
        expected_keys = {
            "template1/subdir",
            "template1/empty",
            "template1/inherit.txt",
            "template1/subdir/subdir.txt",
            "template1",
            "template1/template1.txt",
        }

        # Act
        result = catalog_templates(template1)

        # Assert
        assert set(result.keys()) == expected_keys

        for key in expected_keys:
            assert (tmp_path / key).exists()

    def test_result_values_are_full_paths(self, tmp_path: Path):
        """The returned values are full filepaths as `Path`s."""
        # Assemble
        generate_fake_templates(tmp_path)
        template1 = tmp_path / "template1"

        # Act
        result = catalog_templates(template1)

        # Assert
        for value in result.values():
            assert value.exists()
            assert value.is_absolute()


class TestCatalogInheritance:
    """Tests for the `catalog_inheritance` function."""

    def test_empty_list_results_in_empty_map(self):
        """Cataloging an empty list returns an empty InheritanceMap."""
        result = catalog_inheritance([])
        assert isinstance(result, InheritanceMap)
        assert len(result.maps) == 1
        assert len(result.maps[0]) == 0

    def test_single_path_results_in_one_extra_map(self, tmp_path: Path):
        generate_fake_templates(tmp_path)
        template_paths = [tmp_path / "template1"]
        result = catalog_inheritance(template_paths)
        assert isinstance(result, InheritanceMap)
        assert len(result.maps) == 2, "InheritanceMap should have one child for a single element template_paths list"

    def test_multiple_paths_has_multiple_maps(self, tmp_path: Path):
        generate_fake_templates(tmp_path)
        template_paths = [tmp_path / "template1", tmp_path / "template2"]

        result = catalog_inheritance(template_paths)
        assert isinstance(result, InheritanceMap)
        assert (
            len(result.maps) == len(template_paths) + 1
        ), "Number of children should match number of template paths plus 1"
        assert result.maps[0] == {
            "template2/inherit.txt": tmp_path / "template2/inherit.txt",
            "template2/template2.txt": tmp_path / "template2/template2.txt",
            "template2": tmp_path / "template2",
        }
        assert result.maps[1] == {
            "template1/inherit.txt": tmp_path / "template1/inherit.txt",
            "template1/template1.txt": tmp_path / "template1/template1.txt",
            "template1/subdir/subdir.txt": tmp_path / "template1/subdir/subdir.txt",
            "template1/empty": tmp_path / "template1/empty",
            "template1/subdir": tmp_path / "template1/subdir",
            "template1": tmp_path / "template1",
        }
        assert result.maps[2] == {}
