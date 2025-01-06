"""Tests for project_forge.rendering.render.py."""

from pathlib import Path

import pytest

from project_forge.context_builder.context import build_context
from project_forge.models.composition import read_composition_file
from project_forge.rendering.environment import load_environment
from project_forge.rendering.render import render_env
from project_forge.rendering.templates import catalog_inheritance
from project_forge.ui.terminal import ask_question


@pytest.fixture
def template(tmp_path: Path):
    """A simple template structure."""
    template_dir = tmp_path / "template"
    template_dir.mkdir()
    template_dir.joinpath("{{ repo_name }}").mkdir()
    template_dir.joinpath("{{ repo_name }}", "file.txt").write_text("{{ key }}")
    template_dir.joinpath("{{ repo_name }}", "skipme.txt").write_text("{{ key }}")
    template_dir.joinpath("{{ repo_name }}", "copy_only.txt").write_text("{{ key }}")
    pattern_content = (
        'template_location = "{{ repo_name }}"\n'
        'skip = ["{{ repo_name }}/skipme.txt"]\n'
        'copy_only = ["{{ repo_name }}/copy_only.txt"]\n'
        "[extra_context]\n"
        'key = "value"\n'
    )
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


def assemble_and_render(template: Path, dest_path: Path):
    """Assemble and render an environment."""
    composition = read_composition_file(template / "composition.toml")
    context = build_context(composition, ask_question)
    template_paths = [
        (
            overlay.pattern.template_location.resolve(),
            overlay.pattern.get_process_mode,
        )
        for overlay in composition.steps
    ]
    inheritance = catalog_inheritance(template_paths)
    env = load_environment(inheritance)
    render_env(env, inheritance, context, dest_path)


class TestRenderEnv:
    """Tests for render_env function."""

    def test_renders_a_file_template(self, tmp_path: Path, template: Path):
        """It renders a file template with the correct content."""
        assemble_and_render(template, tmp_path)

        # Assert
        file_path = tmp_path / "my-project" / "file.txt"
        assert file_path.exists()
        assert file_path.read_text() == "value"

    def test_creates_directories(self, tmp_path: Path, template: Path):
        """It creates directories for the rendered files."""
        assemble_and_render(template, tmp_path)

        # Assert
        dir_path = tmp_path / "my-project"
        assert dir_path.exists()

    def test_skips_files(self, tmp_path: Path, template: Path):
        """The files specified in the skip list are skipped."""
        assemble_and_render(template, tmp_path)

        # Assert
        file_path = tmp_path / "my-project" / "skipme.txt"
        assert not file_path.exists()

    def test_copies_files(self, tmp_path: Path, template: Path):
        """The files specified in the copy_only list are copied and not rendered."""
        assemble_and_render(template, tmp_path)

        # Assert
        file_path = tmp_path / "my-project" / "copy_only.txt"
        assert file_path.exists()
        assert file_path.read_text() == "{{ key }}"
