"""Tools and classes for managing the Jinja2 rendering environment."""

import logging
import re
from collections import ChainMap
from pathlib import Path
from typing import Any, Callable, List, Optional

from jinja2 import BaseLoader, Environment, TemplateNotFound, Undefined

logger = logging.getLogger(__name__)


class InheritanceMap(ChainMap[str, Path]):
    """Provides convenience functions for managing template inheritance."""

    @property
    def is_empty(self) -> bool:
        """The context has only one mapping and it is empty."""
        return len(self.maps) == 1 and len(self.maps[0]) == 0

    def inheritance(self, key: str) -> List[Path]:
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
        # Parse the name of the template
        bits = template.split("/", maxsplit=1)
        index = 0
        if len(bits) == 2 and bits[0].isdigit():
            index = int(bits[0])
            template_name = bits[1]
        else:
            template_name = template

        # Get template inheritance
        inheritance = self.templates.inheritance(template_name)
        inheritance_len = len(inheritance)

        if not inheritance:
            raise TemplateNotFound(template_name)

        # Load the template from the index
        if index >= inheritance_len:
            raise TemplateNotFound(template)  # Maybe this wasn't one of our customized extended paths

        path = inheritance[index]
        logger.debug(f"Loading template {template_name} from: {path}")
        source = path.read_text()

        # look for an `extends` tag
        block_start_string = environment.block_start_string
        block_end_string = environment.block_end_string
        regex = re.compile(
            self.extends_re.format(block_start_string=block_start_string, block_end_string=block_end_string)
        )
        if match := regex.search(source):
            if index == len(inheritance) - 1:
                # we've reached our last template, so we must remove the `extends` tag completely
                source = source.replace(match[0], "")
            else:
                # rewrite the `extends` tag to reference the next item in the inheritance
                source = source.replace(match[1], f"{index + 1}/{match[1]}")

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
    return Environment(  # NOQA: S701
        loader=InheritanceLoader(template_map), extensions=extensions, undefined=SuperUndefined
    )
