"""Tasks are commands to run while rendering a composition."""

import os
import subprocess
from pathlib import Path
from typing import Annotated, List, Optional

from pydantic import AfterValidator, BaseModel, Field, model_validator

from project_forge.rendering.expressions import render_bool_expression, render_expression
from project_forge.utils import inside_dir

EnvDict = Annotated[dict[str, str], AfterValidator(lambda v: {key.upper(): str(val) for key, val in v.items()})]


class Task(BaseModel):
    """A task to run while rendering a composition."""

    command: str | List[str] = Field(description="The command to run.")
    use_shell: bool = Field(
        default=False,
        description="Whether to run the command in a shell.\n\nIf `command` is a str, this is always `True`.",
    )
    env: Optional[EnvDict] = Field(
        default=None,
        description=(
            "Environment variables to set when running the command.\n\n"
            "Each environment variable value may be a template string rendered using the context so far."
        ),
    )
    when: Optional[str] = Field(
        default=None, description="A template string that will render as `True` if the task should run."
    )
    context_variable_name: Optional[str] = Field(
        default=None,
        description=(
            "The name of a context variable that will be set to the command's stdout. "
            "If not provided, the the output is not saved to the context."
        ),
    )

    @model_validator(mode="after")
    def validate_use_shell(self) -> "Task":
        """Set `use_shell` to True if command is a str."""
        if isinstance(self.command, str):
            self.use_shell = True
        return self


def execute_task(task: Task, context: dict) -> dict:
    """
    Execute a task.

    Args:
        task: The task to execute
        context: The current context

    Returns:
        The updated context.
    """
    should_execute = render_bool_expression(task.when, context) if task.when else True
    if not should_execute:
        return context

    env = os.environ.copy()
    if task.env:
        extra_env = {key: render_expression(val) for key, val in task.env.items()}
        env |= extra_env

    command = (
        [render_expression(cmd, context) for cmd in task.command]
        if isinstance(task.command, list)
        else render_expression(task.command, context)
    )

    working_dir = context.get("working_dir", Path.cwd())
    with inside_dir(working_dir):
        result = subprocess.run(  # noqa: S603
            command,
            shell=task.use_shell,
            env=env,
            capture_output=True,
            check=True,
        )
        if task.context_variable_name:
            context[task.context_variable_name] = result.stdout.decode("utf-8").strip()

    return context
