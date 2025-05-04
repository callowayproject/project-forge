"""Tests for the `project_forge.testing` module."""

from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

from project_forge.testing import run_inside_dir
from project_forge.ui.defaults import return_defaults


class TestForgerFixture:
    """Tests for the `forger` fixture."""

    def test_forger_class(self, pytester):
        """The `forger` fixture should return a `Forger` class."""
        # Assemble
        pytester.makepyfile(
            """
            def test_forger_fixture(forger):
                assert forger.__class__.__name__ == "Forger"
                assert hasattr(forger, "forge")
                assert hasattr(forger, "inside_dir")
                assert hasattr(forger, "run_inside_dir")
            """
        )

        # Act
        result = pytester.runpytest()

        # Assert
        if result.ret != 0:
            print(result.stdout, result.stderr)

        assert result.ret == 0

    def test_output_dir_setting_is_recognized(self, pytester, tmp_path: Path):
        """The `forger-output-dir` setting should change where the project is built."""
        # Assemble
        output_dir = tmp_path / "test_output"
        output_dir.mkdir(parents=True, exist_ok=True)
        pytester.makepyfile(
            f"""
            def test_forger_fixture(forger):
                assert str(forger._output_dir.as_posix()) == "{output_dir.as_posix()}"
            """
        )

        # Act
        result = pytester.runpytest(f"--forge-output-dir={output_dir}")

        # Assert
        if result.ret != 0:
            print(result.stdout, result.stderr)

        assert result.ret == 0

    def test_raises_error_if_output_dir_setting_is_file(self, pytester, tmp_path: Path):
        """If the `forger-output-dir` is a file, it raises a `ValueError`."""
        # Assemble
        output_dir = tmp_path / "test_output"
        output_dir.touch()
        pytester.makepyfile(
            f"""
            def test_forger_fixture(forger):
                assert str(forger._output_dir.as_posix()) == "{output_dir.as_posix()}"
            """
        )

        # Act
        result = pytester.runpytest(f"--forge-output-dir={output_dir}")

        # Assert
        assert "ValueError: The output path" in result.stdout.str()

    def test_forge_command_renders(self, pytester, tmp_path: Path, fixtures_dir: Path):
        """The forge command properly builds a project."""
        # Assemble
        composition_path = fixtures_dir.joinpath("composition1.toml").resolve()
        composition_path_str = str(composition_path).replace("\\", "\\\\")
        output_dir = tmp_path / "test_output"
        output_dir.mkdir(parents=True, exist_ok=True)
        pytester.makepyfile(
            f"""
            def test_forger_fixture(forger):
                result = forger.forge(config_path="{composition_path_str}")
                assert result.exception == None
                assert result.exit_code == 0
                assert result.project_dir.exists()
                assert len(result.context) > 1
            """
        )

        # Act
        result = pytester.runpytest(f"--forge-output-dir={output_dir}")

        # Assert
        if result.ret != 0:
            print(result.stdout, result.stderr)

        assert result.ret == 0
        assert output_dir.joinpath("my-project").exists()

    @patch("project_forge.testing.run_inside_dir")
    def test_run_inside_dir_calls_function(self, mock_run_inside_dir, pytester):
        """The `run_inside_dir` function should call the `run_inside_dir` function."""
        # Assemble
        mock_run_inside_dir.return_value = CompletedProcess(args=["ls"], returncode=0, stdout=b"list", stderr=b"")
        pytester.makepyfile(
            """
            from pathlib import Path
            def test_forger_fixture(forger):
                result = forger.run_inside_dir("ls", Path("/some/path"))
                assert result.exception == None
                assert result.exit_code == 0
            """
        )

        # Act
        pytester.runpytest()

        # Assert
        mock_run_inside_dir.assert_called_once_with("ls", Path("/some/path"))


class TestRunInsideDir:
    """Tests for the `run_inside_dir` function."""

    @patch("project_forge.testing.subprocess")
    @patch("project_forge.testing.inside_dir")
    def test_run_inside_dir_success(self, mock_inside_dir, mock_subprocess):
        """Test successful execution of a command inside a directory."""
        # Mock the result of subprocess.run
        mock_subprocess.run.return_value = CompletedProcess(args=["ls"], returncode=0, stdout=b"list", stderr=b"")

        # Define the command and directory
        command = "ls"
        dir_path = Path("/some/path")

        # Call the function
        result = run_inside_dir(command, dir_path)

        # Assertions
        mock_inside_dir.assert_called_once_with(dir_path)
        mock_subprocess.run.assert_called_once_with(["ls"], capture_output=True, check=True)
        assert result.returncode == 0
        assert result.stdout == b"list"

    @patch("project_forge.testing.subprocess")
    @patch("project_forge.testing.inside_dir")
    def test_run_inside_dir_failure(self, mock_inside_dir, mock_subprocess):
        """Test failed execution of a command inside a directory."""
        # Mock the result of subprocess.run
        mock_subprocess.run.return_value = CompletedProcess(args=["ls"], returncode=1, stdout=b"", stderr=b"error")

        # Define the command and directory
        command = "ls"
        dir_path = Path("/some/path")

        # Call the function
        result = run_inside_dir(command, dir_path)

        # Assertions
        mock_inside_dir.assert_called_once_with(dir_path)
        mock_subprocess.run.assert_called_once_with(["ls"], capture_output=True, check=True)
        assert result.returncode == 1
        assert result.stderr == b"error"


def test_return_defaults_ui_returns_default():
    """The `return_defaults` UI function only returns the default value."""
    result = return_defaults("Question?", default="yes")
    assert result == "yes"
