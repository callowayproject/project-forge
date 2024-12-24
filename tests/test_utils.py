import contextlib
import os
from pathlib import Path

from project_forge.utils import inside_dir


class TestInsideDir:
    """Tests for the `inside_dir` context manager."""

    def test_inside_dir_changes_directory(self, temp_directory):
        """Test that inside_dir changes the current working directory."""
        initial_directory = Path(os.getcwd())
        with inside_dir(temp_directory):
            assert Path(os.getcwd()) == temp_directory
        assert Path(os.getcwd()) == initial_directory

    def test_inside_dir_restores_directory_on_exception(self, temp_directory):
        """Test that inside_dir restores the directory in case of an exception."""
        initial_directory = Path(os.getcwd())
        with contextlib.suppress(ValueError):
            with inside_dir(temp_directory):
                raise ValueError("Intentional exception")
        assert Path(os.getcwd()) == initial_directory
