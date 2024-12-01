"""Utilities for testing Project Forge patterns and compositions."""

import os
import pathlib
import subprocess
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
import shlex
from subprocess import CompletedProcess
from typing import Generator, Optional, Any, Callable

from project_forge.commands.build import build_project
from project_forge.core.models import QuestionType


@contextmanager
def inside_dir(dir_path: Path) -> Generator[None, None, None]:
    """
    Temporarily switch the current directory to the given path.

    Args:
        dir_path: path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dir_path)
        yield
    finally:
        os.chdir(old_path)


def run_inside_dir(command: str, dir_path: Path) -> CompletedProcess:
    """
    Run a command from inside a given directory, returning the exit status

    Args:
        command: Command string to execute within the directory
        dir_path: String, path of the directory the command is being run.

    Returns:
        The result code of the command.
    """
    with inside_dir(dir_path):
        return subprocess.run(shlex.split(command), capture_output=True, check=True)


def use_default_ui(
    prompt: str,
    type: QuestionType = "str",
    help: Optional[str] = None,
    choices: Optional[dict] = None,
    default: Any = None,
    multiselect: bool = False,
    validator_func: Optional[Callable] = None,
    **kwargs,
) -> Any:
    """A testing UI that simply returns the default answer."""
    return default


@dataclass
class Result:
    """Holds the captured result of the cookiecutter project generation."""

    exception: Optional[BaseException] = None
    exit_code: str | int = 0
    project_dir: Optional[pathlib.Path] = None
    context: Optional[dict] = None


class Forger:
    """Class to provide convenient access to the project_forge API."""

    def __init__(self, output_dir: pathlib.Path):
        self._output_dir = output_dir

    def forge(
        self, config_path: Optional[pathlib.Path], use_defaults: bool = False, initial_context: Optional[dict] = None
    ) -> Result:
        """Build a project from the given config."""
        exception: Optional[BaseException] = None
        exit_code: str | int = 0
        build_result = None

        try:
            build_result = build_project(
                composition_file=config_path,
                output_dir=self._output_dir,
                use_defaults=use_defaults,
                ui_function=use_default_ui,
                initial_context=initial_context,
            )
        except SystemExit as e:  # pragma: no-coverage
            if e.code != 0:
                exception = e
            exit_code = e.code
        except Exception as e:  # pragma: no-coverage
            exception = e
            exit_code = -1

        return Result(
            exception=exception,
            exit_code=exit_code,
            project_dir=build_result.root_path if build_result else None,
            context=build_result.context if build_result else None,
        )
