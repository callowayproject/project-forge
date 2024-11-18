"""Starting point to render a project."""

import logging
from pathlib import Path
from typing import Optional

from project_forge.configurations.composition import read_composition_file
from project_forge.context_builder.context import build_context
from project_forge.rendering.environment import load_environment
from project_forge.rendering.render import render_env
from project_forge.rendering.templates import catalog_inheritance
from project_forge.tui import ask_question

logger = logging.getLogger(__name__)


def build_project(
    composition_file: Path, output_dir: Path, use_defaults: bool = False, initial_context: Optional[dict] = None
) -> None:
    """Render a project to a directory."""
    initial_context = initial_context or {}
    composition = read_composition_file(composition_file)

    if use_defaults:
        for overlay in composition.overlays:
            overlay.ask_questions = False
    context = build_context(composition, ask_question, initial_context)

    template_paths = [overlay.pattern.template_location.resolve() for overlay in composition.overlays]  # type: ignore[union-attr]
    inheritance = catalog_inheritance(template_paths)
    env = load_environment(inheritance)
    render_env(env, inheritance, context, output_dir)
