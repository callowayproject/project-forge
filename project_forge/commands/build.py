"""Starting point to render a project."""

import logging
from pathlib import Path
from typing import Optional

from project_forge.context_builder.context import build_context
from project_forge.core.types import BuildResult, UIFunction
from project_forge.models.composition import read_composition_file
from project_forge.models.overlay import Overlay
from project_forge.rendering.environment import load_environment
from project_forge.rendering.render import render_env
from project_forge.rendering.templates import catalog_inheritance

logger = logging.getLogger(__name__)


def build_project(
    composition_file: Path,
    output_dir: Path,
    ui_function: UIFunction,
    initial_context: Optional[dict] = None,
) -> BuildResult:
    """Render a project to a directory."""
    initial_context = initial_context or {}
    composition = read_composition_file(composition_file)
    overlays = [item for item in composition.steps if isinstance(item, Overlay)]
    context = build_context(composition, ui_function, initial_context)

    template_paths = [
        (overlay.pattern.template_location.resolve(), overlay.pattern.get_process_mode) for overlay in overlays
    ]
    inheritance = catalog_inheritance(template_paths)
    env = load_environment(inheritance)
    root_path = render_env(env, inheritance, context, output_dir)
    return BuildResult(root_path, context)
