"""Data models for configurations."""

from pathlib import Path
from typing import Dict, List, Union

from pydantic import BaseModel, Field

from project_forge.context_builder.data_merge import MergeMethods
from project_forge.core.io import parse_file
from project_forge.models.location import Location
from project_forge.models.overlay import Overlay
from project_forge.models.task import Task


class Composition(BaseModel):
    """The settings for a composition."""

    steps: List[Overlay | Task] = Field(
        default_factory=list, description="A list of pattern overlays and tasks to compose."
    )
    merge_keys: Dict[str, MergeMethods] = Field(
        default_factory=dict,
        description=(
            "Merge the values of one or more keys in a specific way. This is useful for `yaml` or `json` values. "
            "Valid merge methods are `overwrite`, `nested-overwrite`, and `comprehensive`."
        ),
    )
    extra_context: dict = Field(
        default_factory=dict,
        description="Override one or more keys in this pattern's `extra_context`. Values can be a template string.",
    )

    @classmethod
    def from_location(cls, location: Union[str, Location]) -> "Composition":
        """Convert the location to a pattern into a composition."""
        return cls(steps=[Overlay(pattern_location=location)])

    def cache_data(self) -> None:
        """
        Makes sure all the patterns are cached and have their pattern objects loaded.

        Accessing the `pattern` property on an overlay will lazily load the pattern.
        """
        for step in self.steps:
            if hasattr(step, "pattern"):
                _ = step.pattern


def is_composition_data(data: dict) -> bool:
    """Returns True if the data is for a composition, otherwise False."""
    return "steps" in data


def read_composition_file(path: Union[str, Path]) -> Composition:
    """
    Read, parse, and validate the contents of a composition file and patterns.

    If the path is to a pattern file, it is added to a composition and returned.

    Args:
        path: The path to the composition or pattern file

    Returns:
        A resolved and validated composition object.
    """
    data = parse_file(path)
    context = {"composition_path": Path(path).parent}
    if is_composition_data(data):
        composition = Composition.model_validate(data, context=context)
    else:
        composition = Composition.model_validate({"steps": [Overlay(pattern_location=str(path))]}, context=context)

    composition.cache_data()

    return composition
