"""Tests for project_forge.rendering.templates."""

from pathlib import Path

from project_forge.rendering.templates import (
    InheritanceMap,
    ProcessMode,
    TemplateFile,
    catalog_inheritance,
    catalog_templates,
)

RW_MODE = ProcessMode.render | ProcessMode.write


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


def process_mode_func(path: Path) -> ProcessMode:
    """A function to process a mode."""
    return RW_MODE


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
        result = catalog_templates(template1, process_mode_func)

        # Assert
        assert {x.replace("\\", "/") for x in result.keys()} == expected_keys

        for key in expected_keys:
            assert (tmp_path / key).exists()

    def test_result_values_are_full_paths(self, tmp_path: Path):
        """The returned values are full filepaths as `Path`s."""
        # Assemble
        generate_fake_templates(tmp_path)
        template1 = tmp_path / "template1"

        # Act
        result = catalog_templates(template1, process_mode_func)

        # Assert
        for value in result.values():
            assert value.path.exists()
            assert value.path.is_absolute()


class TestCatalogInheritance:
    """Tests for the `catalog_inheritance` function."""

    def test_empty_list_results_in_empty_map(self):
        """Cataloging an empty list returns an empty InheritanceMap."""
        result = catalog_inheritance([])
        assert isinstance(result, InheritanceMap)
        assert len(result.maps) == 1
        assert len(result.maps[0]) == 0

    def test_single_path_results_in_one_extra_map(self, tmp_path: Path):
        """InheritanceMap should have one child for a single element template_paths list."""
        generate_fake_templates(tmp_path)
        template_paths = [(tmp_path / "template1", process_mode_func)]
        result = catalog_inheritance(template_paths)
        assert isinstance(result, InheritanceMap)
        assert len(result.maps) == 2, "InheritanceMap should have one child for a single element template_paths list"

    def test_multiple_paths_has_multiple_maps(self, tmp_path: Path):
        """The number of maps should match the number of template paths plus 1."""
        generate_fake_templates(tmp_path)
        template_paths = [(tmp_path / "template1", process_mode_func), (tmp_path / "template2", process_mode_func)]

        result = catalog_inheritance(template_paths)
        assert isinstance(result, InheritanceMap)
        assert len(result.maps) == len(template_paths) + 1, (
            "Number of children should match number of template paths plus 1"
        )
        assert result.maps[0] == {
            "template2/inherit.txt": TemplateFile(tmp_path / "template2/inherit.txt", RW_MODE),
            "template2/template2.txt": TemplateFile(tmp_path / "template2/template2.txt", RW_MODE),
            "template2": TemplateFile(tmp_path / "template2", RW_MODE),
        }
        assert result.maps[1] == {
            "template1/inherit.txt": TemplateFile(tmp_path / "template1/inherit.txt", RW_MODE),
            "template1/template1.txt": TemplateFile(tmp_path / "template1/template1.txt", RW_MODE),
            "template1/subdir/subdir.txt": TemplateFile(tmp_path / "template1/subdir/subdir.txt", RW_MODE),
            "template1/empty": TemplateFile(tmp_path / "template1/empty", RW_MODE),
            "template1/subdir": TemplateFile(tmp_path / "template1/subdir", RW_MODE),
            "template1": TemplateFile(tmp_path / "template1", RW_MODE),
        }
        assert result.maps[2] == {}
