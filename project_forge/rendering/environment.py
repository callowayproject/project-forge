"""Tools and classes for managing the Jinja2 rendering environment."""

import logging
import re
from dataclasses import dataclass
from typing import Any, Callable, Optional

from jinja2 import BaseLoader, Environment, TemplateNotFound, Undefined

from project_forge.rendering.templates import InheritanceMap

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class InheritanceRef:
    """A parsed reference to one rung of a template's inheritance chain.

    `InheritanceLoader` addresses a specific ancestor of a template with an
    `"{index}/{name}"` string (e.g. `"2/a.txt"`); this is the value object for that string.
    """

    name: str
    index: int = 0

    @classmethod
    def parse(cls, template: str) -> "InheritanceRef":
        """Parse a loader template name, e.g. `"2/a.txt"` or the un-prefixed `"a.txt"`."""
        bits = template.split("/", maxsplit=1)
        if len(bits) == 2 and bits[0].isdigit():
            return cls(name=bits[1], index=int(bits[0]))
        return cls(name=template)

    def format(self) -> str:
        """Render this reference back into the loader's `"{index}/{name}"` string form."""
        return f"{self.index}/{self.name}"


class SuperUndefined(Undefined):
    """Let calls to super() work ok."""

    def __getattr__(self, name: str) -> Any:
        """Override the superclass' __getattr__ method to handle the `jinja_pass_arg` attribute."""
        if name.startswith("__"):
            raise AttributeError(name)
        return False if name == "jinja_pass_arg" else self._fail_with_undefined_error()

    def __call__(self) -> str:
        """If the undefined is called (like super()) it outputs an empty string."""
        return ""


class InheritanceLoader(BaseLoader):
    """Load templates from inherited templates of the same name."""

    extends_re: str = "{block_start_string}\\s*extends\\s*[\"']([^\"']+)[\"']\\s*{block_end_string}"

    def __init__(self, inheritance_map: InheritanceMap):
        self.templates = inheritance_map

    def get_source(self, environment: Environment, template: str) -> tuple[str, str | None, Callable[[], bool] | None]:
        """Load the template."""
        ref = InheritanceRef.parse(template)

        # Get template inheritance
        inheritance = self.templates.inheritance(ref.name)
        inheritance_len = len(inheritance)

        if not inheritance:
            raise TemplateNotFound(ref.name)

        # Load the template from the index
        if ref.index >= inheritance_len:
            raise TemplateNotFound(template)  # Maybe this wasn't one of our customized extended paths

        template_file = inheritance[ref.index]

        if not template_file.is_renderable:
            raise TemplateNotFound(template)

        path = template_file.path
        logger.debug(f"Loading template {ref.name} from: {path}")
        source = path.read_text()

        # look for an `extends` tag
        block_start_string = environment.block_start_string
        block_end_string = environment.block_end_string
        regex = re.compile(
            self.extends_re.format(block_start_string=block_start_string, block_end_string=block_end_string)
        )
        if match := regex.search(source):
            if ref.index == inheritance_len - 1:
                # we've reached our last template, so we must remove the `extends` tag completely
                source = source.replace(match[0], "")
            else:
                # rewrite the `extends` tag to reference the next item in the inheritance
                extended_ref = InheritanceRef(name=match[1], index=ref.index + 1)
                source = source.replace(match[1], extended_ref.format())

        return source, None, lambda: True


def load_environment(template_map: Optional[InheritanceMap] = None, extensions: Optional[list] = None) -> Environment:
    """
    Load the Jinja2 template environment.

    Args:
        template_map: The template inheritance used to load the templates
        extensions: A list of Jinja extensions to load into the environment

    Returns:
        The Jinja environment
    """
    template_map = template_map or InheritanceMap()
    extensions = extensions or []
    return Environment(  # ruff: ignore[jinja2-autoescape-false]
        loader=InheritanceLoader(template_map), extensions=extensions, undefined=SuperUndefined
    )
