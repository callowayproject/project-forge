"""Utilities for testing the rendering of projects."""

import pathlib

import pytest
from _pytest.fixtures import FixtureRequest

from project_forge.testing import Forger


@pytest.fixture
def forger(request: FixtureRequest, tmp_path: pathlib.Path):
    """
    Yield an instance of the Forger helper class that can be used to generate a project from a template.
    """
    output_path = request.config.getoption("forge_output_dir") or tmp_path
    if output_path.is_file():
        raise ValueError(f"The output path {output_path} is a file, not a directory.")
    output_path.mkdir(parents=True, exist_ok=True)
    yield Forger(output_path)


def pytest_addoption(parser):
    """Add the --forge-output-dir option to the pytest command line."""
    group = parser.getgroup("forger")
    group.addoption(
        "--forge-output-dir",
        action="store",
        required=False,
        dest="forge_output_dir",
        help="store rendered projects here",
        type=pathlib.Path,
    )
