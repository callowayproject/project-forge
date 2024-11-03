"""Management of templates."""

from pathlib import Path
from typing import Dict, List

from project_forge.rendering.environment import InheritanceMap


def catalog_templates(template_dir: Path) -> Dict[str, Path]:
    """
    Catalog templates into a dictionary.

    This creates a mapping of a relative file name to a full path.

    For a file structure like:

        /path-to-templates/
            {{ repo_name }}/
                file1.txt
                subdir/
                    file2.txt
                empty-subdir/

    A call to `catalog_templates(Path("/path-to-templates"))` would return:

        {
            "{{ repo_name }}": Path("/path-to-templates/{{ repo_name }}"),
            "{{ repo_name }}/file1.txt": Path("/path-to-templates/{{ repo_name }}/file1.txt"),
            "{{ repo_name }}/subdir": Path("/path-to-templates/{{ repo_name }}/subdir"),
            "{{ repo_name }}/subdir/file2.txt": Path("/path-to-templates/{{ repo_name }}/subdir/file2.txt"),
            "{{ repo_name }}/empty-subdir": Path("/path-to-templates/{{ repo_name }}/empty-subdir"),
        }

    Args:
        template_dir: The directory to catalog

    Returns:
        A mapping of the relative path as a string to the full path
    """
    templates = {}
    for root, dirs, files in template_dir.walk():
        for file in files:
            template_path = root / file
            templates[str(template_path.relative_to(template_dir))] = template_path
        for dir_ in dirs:
            template_path = root / dir_
            templates[str(template_path.relative_to(template_dir))] = template_path
    return {key: templates[key] for key in sorted(templates)}


def catalog_inheritance(template_paths: List[Path]) -> InheritanceMap:
    """Create an InheritanceMap that reflects the inheritance of all the template paths."""
    inheritance = InheritanceMap()
    for template_path in template_paths:
        inheritance = inheritance.new_child(catalog_templates(template_path))
    return inheritance
