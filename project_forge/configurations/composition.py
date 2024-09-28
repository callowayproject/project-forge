"""Data models for configurations."""

from pathlib import Path
from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from project_forge.configurations.pattern import Pattern, read_pattern_file
from project_forge.core.exceptions import PathNotFoundError, RepoAuthError, RepoNotFoundError
from project_forge.core.io import parse_file
from project_forge.core.location import Location

SkippedHook = Literal["pre", "post", "all", "none"]
"""Types of hooks to skip."""

MergeMethods = Literal["overwrite", "nested-overwrite", "comprehensive"]
"""Types of merge methods."""


class Overlay(BaseModel):
    """An object describing how to overlay a pattern in a composition."""

    pattern_location: Union[str, Location] = Field(description="The location of the pattern file for this overlay.")
    _pattern: Optional[Pattern] = None

    #
    # Input manipulation
    #
    ask_questions: bool = Field(
        default=True, description="Ask the user this pattern's questions? When false, the defaults are used."
    )
    defaults: dict = Field(
        default_factory=dict,
        description="Override one or more question's default values in this pattern. Values can be a template string.",
    )
    extra_context: dict = Field(
        default_factory=dict,
        description="Override one or more keys in this pattern's `extra_context`. Values can be a template string.",
    )
    answer_map: dict = Field(
        default_factory=dict,
        description=(
            "This signifies that a previous overlay has already answered one or more of this pattern's questions. "
            "The key is this pattern's question name and the value is a template string that references or modifies "
            "a previous pattern's question name."
        ),
    )

    #
    # File generation
    #
    overwrite_files: List[str] = Field(
        default_factory=list,
        description=(
            "A list of paths or glob patterns of files that may be overwritten. "
            "An empty list means do not overwrite any files."
        ),
    )
    exclude_files: List[str] = Field(
        default_factory=list,
        description=(
            "A list of paths or glob patterns of files to exclude from the generation "
            "(overrides the pattern's configuration)"
        ),
    )
    skip_hooks: SkippedHook = Field(
        default="none", description="Which hooks to skip? Valid options are `all`, `none`, `pre`, `post`."
    )

    @field_validator("pattern_location")
    @classmethod
    def validate_pattern_location(cls, value: Union[str, Location], info: ValidationInfo) -> Location:
        """Check that the pattern_location exists."""
        return _validate_pattern_location(value, info)  # pragma: no-coverage

    @property
    def pattern(self) -> Pattern:
        """Lazy loading of the pattern from its location."""
        if self._pattern is None:
            self._pattern = read_pattern_file(self.pattern_location.resolve())  # type: ignore[union-attr]
        return self._pattern


def _validate_pattern_location(value: Union[str, Location], info: ValidationInfo) -> Location:
    """Check that the pattern location exists."""
    context = info.context
    if isinstance(value, str):
        value = Location.from_string(value)

    pattern_path = Path.cwd()
    if context and "composition_path" in context:
        pattern_path = (
            context["composition_path"].parent
            if context["composition_path"].is_file()
            else context["composition_path"]
        )

    try:
        local_path = value.resolve(pattern_path)
        if not local_path.is_file():
            raise PathNotFoundError(f"The pattern file at {value} is not a file.")
        return value
    except (RepoNotFoundError, RepoAuthError, PathNotFoundError) as e:
        raise ValueError(str(e)) from e


class Composition(BaseModel):
    """The settings for a composition."""

    overlays: List[Overlay] = Field(default_factory=list, description="A list of pattern overlays to compose.")
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
        return cls(overlays=[Overlay(pattern_location=location)])

    def cache_data(self) -> None:
        """Makes sure all the patterns are cached and have their pattern objects loaded."""
        for overlay in self.overlays:
            _ = overlay.pattern


def is_composition_data(data: dict) -> bool:
    """Returns True if the data is for a composition, otherwise False."""
    return "overlays" in data


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
        composition = Composition.model_validate({"overlays": [Overlay(pattern_location=str(path))]}, context=context)

    composition.cache_data()

    return composition
