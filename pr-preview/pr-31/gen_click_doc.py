"""Generate the documentation for the click interface."""

import sys
from pathlib import Path

import mkdocs_gen_files
from mkdocs_click._docs import make_command_docs  # noqa: PLC2701

project_dir = Path(__file__).parent.parent
full_doc_path = "cli.md"

sys.path.insert(0, str(project_dir))

from project_forge.cli import cli  # noqa: E402

lines = list(make_command_docs(prog_name="project-forge", command=cli, style="table", depth=1))

with mkdocs_gen_files.open(full_doc_path, "w") as fd:
    fd.write("# Command Line Interface\n" + "\n".join(lines))
