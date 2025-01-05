"""Functions to render a composition using answered questions."""

import logging
from pathlib import Path

from jinja2 import Environment

from project_forge.rendering.expressions import render_expression
from project_forge.rendering.templates import InheritanceMap

logger = logging.getLogger(__name__)


def render_env(env: Environment, path_list: InheritanceMap, context: dict, destination_path: Path) -> Path:
    """Render the templates in path_list using context."""
    project_root = None

    for path, val in path_list.items():
        dst_rel_path = render_expression(path, context)
        full_path = destination_path / dst_rel_path
        if project_root is None:
            project_root = full_path

        if val.path.is_file():
            logger.debug(f"Writing file {dst_rel_path}")
            full_path.parent.mkdir(parents=True, exist_ok=True)
            if val.is_renderable:
                template = env.get_template(path)
                full_path.write_text(template.render(context))
            else:
                full_path.write_text(val.path.read_text())
        elif val.path.is_dir():
            logger.debug(f"Writing directory {dst_rel_path}")
            full_path.mkdir(parents=True, exist_ok=True)
        else:
            raise ValueError(f"Path {val.path} does not exist")
    return project_root
