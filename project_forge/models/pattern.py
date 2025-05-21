"""
Model definitions relating to Pattern configurations.

A _pattern_ consists of a set of template files and a configuration file. The configuration file defines the context
required to render the template and the rendering rules.

*Patterns* are meant to be focused and reusable. *Patterns* are combined with other *patterns* using a *composition.*

*Patterns* are renderable as-is. They do not need to be a part of a composition.
"""

from pathlib import Path
from typing import Any, Dict, List, Union

from pydantic import BaseModel, Field, ValidationInfo, field_validator, model_validator

from project_forge.core.exceptions import PathNotFoundError, RepoAuthError, RepoNotFoundError
from project_forge.core.io import parse_file
from project_forge.core.types import VARIABLE_REGEX, QuestionType, ScalarType, TemplateEngine
from project_forge.core.validators import is_bool, is_float, is_int
from project_forge.models.location import Location
from project_forge.path_matching import matches_any_glob
from project_forge.rendering.templates import ProcessMode
from project_forge.settings import get_settings


class Choice(BaseModel):
    """A choice to a Question."""

    label: str = Field(pattern=VARIABLE_REGEX, description="The label for this choice when prompted to the user.")
    value: ScalarType = Field(
        description="The value used when this choice is selected. It should match the questions's type."
    )
    skip_when: str = Field(
        default="",
        description=(
            "A template string that will render as `True` if the choice is not valid based on previous context "
            "values.\n\n"
            "Take care to have at least one option without a `skip_when` clause to avoid accidentally creating "
            "a situation with no valid choices."
        ),
    )

    @model_validator(mode="before")
    @classmethod
    def convert_scalar_to_choice(cls, value: Any) -> Any:
        """Convert a scalar value to a Choice object."""
        result_dict = {}
        if not isinstance(value, dict):
            result_dict["value"] = value
        else:
            result_dict = value.copy()

        if "label" not in result_dict or not result_dict["label"]:
            label = str(result_dict["value"]).replace(" ", "_").replace(".", "_")
            if label[0].isdigit():
                label = f"_{label}"
            result_dict["label"] = label

        return result_dict


QUESTION_TYPE_VALIDATORS = {
    "int": is_int,
    "float": is_float,
    "bool": is_bool,
    # Since the choice value is already a string, it is True
    "str": lambda x: True,
    "multiline": lambda x: True,
    "secret": lambda x: True,
    "yaml": lambda x: True,
    "json": lambda x: True,
}

QuestionChoices = Union[List[Choice], List[int], List[float], List[str], List[bool]]


class Question(BaseModel):
    """A question for a pattern."""

    name: str = Field(pattern=VARIABLE_REGEX, description="The name of the variable used in the template.")
    type: QuestionType = Field(default="str", description="The type of this variable.")
    prompt: str = Field(
        default="",
        description=(
            "The message to ask the user for this information. "
            "If no prompt is provided, 'What is the <name>?' is used."
        ),
        validate_default=True,
    )
    help: str = Field(default="", description="Additional information to explain how to answer this question.")
    choices: List[Choice] = Field(default_factory=list, description="A list of choice values or `choice` objects")
    multiselect: bool = Field(
        default=False,
        description=(
            "When `true` allow multiple selections. "
            "The type of this context element will then be a list of this question's `type`"
        ),
    )
    default: Any = Field(
        default=None,
        description=(
            "Provide a default to save them from typing. \n\n"
            "When using `choices`, the default must be the choice _value_, not its _key_, and must match its _type_. "
            "Leave this empty to force the user to answer.\n\n"
            "This value may also be a template string rendered using the context so far. "
            "This allows you to provide defaults based on previous context elements."
        ),
    )

    # TODO[#6]: How to do a basic regex or other string pattern validation?

    validator: str = Field(
        default="",
        description=(
            "Template string to validate the user input. \n\n"
            "This template is rendered using the context so far; it should render _nothing_ if the value is valid "
            "and an error message to show to the user otherwise."
        ),
    )
    force_default: Union[str, bool] = Field(
        default=False,
        description=(
            "A condition that, if `True`, will not prompt the user for a value and uses the `default`.\n\n"
            "`bool` values are used directly. "
            "Setting this to `True` is a good way to make this value a computed value.\n\n"
            "`str` values should be template strings that evaluate to a boolean value."
        ),
    )

    @model_validator(mode="after")
    def use_name_if_missing_prompt(self) -> "Question":
        """Use the name of the question as the prompt if prompt is empty."""
        self.prompt = self.prompt or self.name
        return self

    @model_validator(mode="after")
    def choice_values_match_question_type(self) -> "Question":
        """Ensure that all choice values match this question's type."""
        validator = QUESTION_TYPE_VALIDATORS.get(self.type)
        is_valid = []

        for choice in self.choices:
            if isinstance(choice, Choice):
                is_valid.append(validator(choice.value))
            else:
                is_valid.append(validator(choice))

        types_match = all(is_valid)
        if not types_match:
            raise ValueError(f"Choice values must match the question type: {self.type}")
        return self


class Pattern(BaseModel):
    """The configuration of a pattern."""

    questions: List[Question] = Field(
        default_factory=list,
        description="A list of question objects that define the available context variables for project generation.",
    )
    template_location: Location = Field(
        description=(
            "The location of the root directory of the templates. "
            "This directory's name will be rendered using the context. "
        ),
        validate_default=True,
    )
    extra_context: Dict[str, Any] = Field(
        default_factory=dict, description="Static Key-Values. Values may be template strings."
    )
    template_engine: TemplateEngine = Field(
        default="default", description="The template engine required to render the templates."
    )
    template_engine_ops: Dict[str, Any] = Field(
        default_factory=dict, description="Options to pass to the template engine before rendering."
    )
    skip: List[str] = Field(
        default_factory=list,
        description="A list of paths or glob patterns of files to exclude from writing to the destination.",
    )
    copy_only: List[str] = Field(
        default_factory=list,
        description="A list of paths or glob patterns of files to write to the destination without rendering.",
    )
    migrations: List = Field(default_factory=list, description="TBD")

    @field_validator("template_location", mode="before")
    @classmethod
    def validate_template_location(cls, value: Union[str, Location], info: ValidationInfo) -> Location:
        """Check that the template_location exists."""
        return _validate_template_location(value, info)  # pragma: no-coverage

    def get_process_mode(self, path: Path) -> ProcessMode:
        """Calculates the process mode for a path based on the pattern's skip and copy_only attributes."""
        settings = get_settings()
        mode = ProcessMode.render | ProcessMode.write
        skip_patterns = self.skip + settings.always_skip

        if matches_any_glob(path, skip_patterns):
            mode &= ~ProcessMode.write
        if matches_any_glob(path, self.copy_only):
            mode &= ~ProcessMode.render

        return mode


def _validate_template_location(value: Union[str, Location], info: ValidationInfo) -> Location:
    """Check that the template_path exists."""
    context = info.context
    if isinstance(value, str):
        value = Location.from_string(value)

    pattern_path = Path.cwd()
    if context and "pattern_path" in context:
        pattern_path = context.get("pattern_path")

    try:
        local_path = value.resolve(pattern_path)
        if local_path.exists():
            return value
        else:
            raise ValueError(f"The path {local_path} does not exist.")
    except (RepoNotFoundError, RepoAuthError, PathNotFoundError) as e:
        raise ValueError(str(e)) from e


def find_template_root(root_path: Path, prefix: str = "{{") -> Path:
    """Search for a directory within `root_path` that starts with `prefix`."""
    if not root_path.exists():
        raise PathNotFoundError(f"The root path {root_path} does not exist.")

    if root_path.name.startswith(prefix):
        return root_path

    try:
        for item in root_path.glob(f"{prefix}*"):
            if item.is_dir():
                return item
            continue
    except OSError as e:  # pragma: no-coverage
        raise PathNotFoundError(f"An OS error ({e}) occurred while looking for the template root.") from e

    raise PathNotFoundError(f"Could not find a directory in {root_path} starting with {prefix}.")


def read_pattern_file(path: Union[str, Path]) -> Pattern:
    """Read, parse, and validate the contents of a pattern file."""
    path = Path(path)
    pattern_data = parse_file(path)
    return Pattern.model_validate(pattern_data, context={"pattern_path": path.parent})
