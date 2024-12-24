"""The command-line interface."""

from pathlib import Path
from typing import Any, Optional

import rich_click as click
from click.core import Context

from project_forge import __version__
from project_forge.core.io import parse_file
from project_forge.tui import ask_question


@click.group(
    context_settings={
        "help_option_names": ["-h", "--help"],
    },
    add_help_option=True,
)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx: Context) -> None:
    """Generate projects from compositions and patterns."""
    pass


@cli.command()
@click.argument(
    "composition",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True, path_type=Path),
)
@click.option(
    "--use-defaults",
    is_flag=True,
    help="Do not prompt for input and use the defaults specified in the composition.",
)
@click.option(
    "--output-dir",
    "-o",
    required=False,
    default=lambda: Path.cwd(),  # NOQA: PLW0108
    type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True, path_type=Path),
    help="The directory to render the composition to. Defaults to the current working directory.",
)
@click.option(
    "--data-file",
    "-f",
    required=False,
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True, path_type=Path),
    help=(
        "The path to a JSON, YAML, or TOML file whose contents are added to the initial context. "
        "Great for answering some or all the answers for a composition."
    ),
)
@click.option(
    "--data",
    "-d",
    nargs=2,
    type=str,
    metavar="KEY VALUE",
    required=False,
    multiple=True,
    help="The key-value pairs added to the initial context. Great for providing answers to composition questions.",
)
def build(
    composition: Path,
    use_defaults: bool,
    output_dir: Path,
    data_file: Optional[Path] = None,
    data: Optional[tuple[tuple[str, str], ...]] = None,
):
    """Build a project from a composition and render it to a directory."""
    from project_forge.commands.build import build_project

    initial_context: dict[str, Any] = {"output_dir": output_dir.resolve()}
    if data_file:
        values = parse_file(data_file)
        initial_context |= values or {}

    if data:
        initial_context |= dict(data)

    build_project(
        composition,
        output_dir=output_dir,
        ui_function=ask_question,
        use_defaults=use_defaults,
        initial_context=initial_context,
    )
