"""Functions to render a composition using answered questions."""

import logging
import pprint
from io import StringIO
from pathlib import Path

from jinja2 import Environment

from project_forge.rendering.environment import InheritanceMap
from project_forge.rendering.expressions import render_expression

logger = logging.getLogger(__name__)


def render_env(env: Environment, path_list: InheritanceMap, context: dict, destination_path: Path):
    """Render the templates in path_list using context."""
    context_stream = StringIO()
    pprint.pprint(context, context_stream)
    logger.debug(f"Rendering templates using context:\n{context_stream.getvalue()}")

    for path, val in path_list.items():
        dst_rel_path = render_expression(path, context)
        full_path = destination_path / dst_rel_path

        if not val.exists():
            raise ValueError(f"Path {path} does not exist")

        if val.is_file():
            logger.debug(f"Writing file {dst_rel_path}")
            template = env.get_template(path)
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(template.render(context))
        elif val.is_dir():
            logger.debug(f"Writing directory {dst_rel_path}")
            full_path.mkdir(parents=True, exist_ok=True)
        else:
            raise ValueError(f"Path {val} does not exist")
