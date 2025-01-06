"""Management of templates."""

from collections import ChainMap
from dataclasses import dataclass
from enum import IntFlag, auto
from pathlib import Path
from typing import Callable, Dict, Sequence


class ProcessMode(IntFlag):
    """
    Ways to process the template.

    This is a bitmask, so you can combine them.
    """

    ignore = 0
    """Do not include the template in the inheritance map."""

    render = auto()
    """Process the contents of the template using the template engine."""

    write = auto()
    """Write the contents of the template to the output directory."""


ProcessModeFn = Callable[[Path], ProcessMode]


@dataclass
class TemplateFile:
    """The template file data model."""

    path: Path
    """The full path to the template file."""

    process_mode: ProcessMode = ProcessMode.render | ProcessMode.write
    """How to process the template file."""

    @property
    def is_renderable(self) -> bool:
        """Is the template file renderable?"""
        return self.process_mode & ProcessMode.render != 0

    @property
    def is_writable(self) -> bool:
        """Is the template file writable?"""
        return self.process_mode & ProcessMode.write != 0


def catalog_templates(template_path: Path, process_mode_func: ProcessModeFn) -> Dict[str, TemplateFile]:
    """
    Catalog templates into a dictionary.

    This creates a mapping of a relative file name to a full path.

    For a file structure like:

        {{ repo_name }}/
            file1.txt
            subdir/
                file2.txt
            empty-subdir/

    A call to `catalog_templates(Path("/path-to-templates/{{ repo_name }}/"), process_mode_fn)` would return:

        {
            "{{ repo_name }}": TemplateFile(
                Path("/path-to-templates/{{ repo_name }}"), <ProcessMode.render|write: 3>
            ),
            "{{ repo_name }}/file1.txt": TemplateFile(
                Path("/path-to-templates/{{ repo_name }}/file1.txt"), <ProcessMode.render|write: 3>
            ),
            "{{ repo_name }}/subdir": TemplateFile(
                Path("/path-to-templates/{{ repo_name }}/subdir"), <ProcessMode.render|write: 3>
            ),
            "{{ repo_name }}/subdir/file2.txt": TemplateFile(
                Path("/path-to-templates/{{ repo_name }}/subdir/file2.txt"), <ProcessMode.render|write: 3>
            ),
            "{{ repo_name }}/empty-subdir": TemplateFile(
                Path("/path-to-templates/{{ repo_name }}/empty-subdir"), <ProcessMode.render|write: 3>
            ),
        }

    Args:
        template_path: The directory to catalog
        process_mode_func: A function that takes a path and returns a ProcessMode

    Returns:
        A mapping of the relative path as a string to the full path
    """
    root_dir = template_path.parent
    templates = {template_path.name: TemplateFile(template_path, ProcessMode.render | ProcessMode.write)}
    for root, dirs, files in template_path.walk():
        for file in files:
            template_path = root / file
            process_mode = process_mode_func(template_path)
            templates[str(template_path.relative_to(root_dir).as_posix())] = TemplateFile(template_path, process_mode)
        for dir_ in dirs:
            # TODO: Handle directory inheritance of ProcessModes
            template_path = root / dir_
            process_mode = process_mode_func(template_path)
            templates[str(template_path.relative_to(root_dir).as_posix())] = TemplateFile(template_path, process_mode)
    return {key: templates[key] for key in sorted(templates)}


class InheritanceMap(ChainMap[str, TemplateFile]):
    """Provides convenience functions for managing template inheritance."""

    @property
    def is_empty(self) -> bool:
        """The context has only one mapping and it is empty."""
        return len(self.maps) == 1 and len(self.maps[0]) == 0

    def inheritance(self, key: str) -> list[TemplateFile]:
        """
        Show all the values associated with a key, from most recent to least recent.

        If the maps were added in the order `{"a": Path("1")}, {"a": Path("2")}, {"a": Path("3")}`,
        The output for `inheritance("a")` would be `[Path("3"), Path("2"), Path("1")]`.

        Args:
            key: The key to look up

        Returns:
            The values for that key with the last value first.
        """
        return [mapping[key] for mapping in self.maps[::-1] if key in mapping]


def catalog_inheritance(template_info: Sequence[tuple[Path, ProcessModeFn]]) -> InheritanceMap:
    """Create an InheritanceMap that reflects the inheritance of all the template paths."""
    inheritance = InheritanceMap()
    for template_path, process_mode_func in template_info:
        inheritance = inheritance.new_child(catalog_templates(template_path, process_mode_func))
    return inheritance
