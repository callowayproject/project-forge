"""The command-line interface."""

from pathlib import Path
from typing import Any, Optional

import rich_click as click
from click.core import Context

from project_forge import __version__
from project_forge.core.io import parse_file
from project_forge.core.urls import parse_git_url
from project_forge.ui.defaults import return_defaults
from project_forge.ui.terminal import ask_question


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
    type=str,
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
    composition: str,
    use_defaults: bool,
    output_dir: Path,
    data_file: Optional[Path] = None,
    data: Optional[tuple[tuple[str, str], ...]] = None,
):
    """Build a project from a composition and render it to a directory."""
    from project_forge.commands.build import build_project

    parsed_url = parse_git_url(composition)
    composition_path = Path(parsed_url.full_path)

    initial_context: dict[str, Any] = {"output_dir": output_dir.resolve()}
    if data_file:
        values = parse_file(data_file)
        initial_context |= values or {}

    if data:
        initial_context |= dict(data)

    ui_function = return_defaults if use_defaults else ask_question

    build_project(
        composition_path,
        output_dir=output_dir,
        ui_function=ui_function,
        initial_context=initial_context,
    )


@cli.command()
@click.argument(
    "OUTPUT_DIR",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        writable=True,
        path_type=Path,
    ),
)
def write_schemas(output_dir: Path):
    """
    Write the JSON schemas for compositions and patterns to the specified output directory.

    The JSON schemas are used by IDEs to provide validation and autocompletion.
    The output directory must exist and be writable by the user.
    """
    from project_forge.commands.export_schemas import export_schemas

    result = export_schemas()

    composition_path = output_dir / "composition.schema.json"
    composition_path.write_text(result.composition_schema)

    pattern_path = output_dir / "pattern.schema.json"
    pattern_path.write_text(result.pattern_schema)
