"""Configuration and utilities for PyTest."""

from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import pytest


@contextmanager
def inside_dir(dirpath: Path) -> Generator:
    """
    Temporarily switch to a specific directory.

    Args:
        dirpath: Path of the directory to switch to
    """
    import os

    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@pytest.fixture
def fixtures_dir() -> Path:
    """Provide the path to the fixture directory."""
    tests_dir = Path(__file__).parent
    return tests_dir / "fixtures"
