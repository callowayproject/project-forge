"""An object describing how to apply a pattern to a composition."""

from pathlib import Path
from typing import List, Optional, Union

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from project_forge.core.exceptions import PathNotFoundError, RepoAuthError, RepoNotFoundError
from project_forge.models.location import Location
from project_forge.models.pattern import Pattern, read_pattern_file


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
