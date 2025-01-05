"""Tests for project_forge.rendering.render.py."""

from pathlib import Path

import pytest

from project_forge.models.composition import read_composition_file
from project_forge.rendering.environment import load_environment
from project_forge.rendering.render import render_env
from project_forge.context_builder.context import build_context
from project_forge.rendering.templates import catalog_inheritance
from project_forge.ui.terminal import ask_question


@pytest.fixture
def template(tmp_path: Path):
    """A simple template structure."""
    template_dir = tmp_path / "template"
    template_dir.mkdir()
    template_dir.joinpath("{{ repo_name }}").mkdir()
    template_dir.joinpath("{{ repo_name }}", "file.txt").write_text("{{ key }}")
    pattern_content = 'template_location = "{{ repo_name }}"\n[extra_context]\nkey = "value"\n'
    template_dir.joinpath("pattern.toml").write_text(pattern_content)
    composition_content = "\n".join(
        [
            "steps = [",
            '  { pattern_location = "pattern.toml" }',
            "]",
            "[extra_context]",
            'repo_name = "my-project"',
        ]
    )
    template_dir.joinpath("composition.toml").write_text(composition_content)
    return template_dir


def test_render_env_for_file(tmp_path: Path, template: Path):
    # Assemble
    composition = read_composition_file(template / "composition.toml")
    context = build_context(composition, ask_question)
    template_paths = [overlay.pattern.template_location.resolve() for overlay in composition.steps]
    inheritance = catalog_inheritance(template_paths)
    env = load_environment(inheritance)

    # Act
    render_env(env, inheritance, context, tmp_path)

    # Assert
    file_path = tmp_path / "my-project" / "file.txt"
    assert file_path.exists()
    assert file_path.read_text() == "value"


def test_render_env_for_directory(tmp_path: Path, template: Path):
    # Assemble
    composition = read_composition_file(template / "composition.toml")
    context = build_context(composition, ask_question)
    template_paths = [overlay.pattern.template_location.resolve() for overlay in composition.steps]
    inheritance = catalog_inheritance(template_paths)
    env = load_environment(inheritance)

    # Act
    render_env(env, inheritance, context, tmp_path)

    # Assert
    dir_path = tmp_path / "my-project"
    assert dir_path.exists()
