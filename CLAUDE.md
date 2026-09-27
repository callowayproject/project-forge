# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install all dependency groups
uv sync --all-groups

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_core/test_indented_logger.py

# Run a single test by name
uv run pytest tests/test_core/test_indented_logger.py::test_function_name

# Lint (check only)
ruff check .

# Format check
ruff format --check .

# Auto-fix lint and format
ruff check --fix . && ruff format .

# Type checking
mypy project_forge

# Install pre-commit hooks (one-time setup)
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files
```

## Architecture

Project Forge generates code projects by composing multiple template patterns. The mental model: **Compositions** are recipes, **Patterns** are ingredients, **Overlays** define how each pattern gets applied, and **Tasks** are side effects during generation.

### Data Flow

```
Composition (YAML/TOML config)
    → build_context() — collects user input via UIFunction, builds context dict
    → render_env()    — renders Jinja2 templates using context
    → output files
```

### Key Modules

- **`models/`** — Pydantic models: `Composition`, `Pattern`, `Overlay`, `Task`, `Location`. These map directly to the configuration file structure.
- **`context_builder/`** — Builds the rendering context. `context.py:build_context()` is the main entry point: starts with `{"now": datetime}`, renders `extra_context`, then processes each `Overlay` or `Task` step sequentially.
- **`rendering/`** — Jinja2-based template rendering. `templates.py` builds an `InheritanceMap` (ordered dict of destination-path → template-path) that supports overlay layering. `render.py:render_env()` walks the map and writes files.
- **`commands/build.py`** — Wires together context building and rendering; called by the CLI.
- **`ui/`** — The `UIFunction` protocol (`core/types.py`) abstracts user interaction. `terminal.py` is the interactive implementation; `defaults.py` returns defaults non-interactively (used with `--use-defaults`).
- **`testing/plugin.py`** — Registers the `forger` pytest fixture, which renders a composition and returns the output for assertions. Activated via the `pytest11` entry point.

### Template Processing Modes

Each template file has a bitmask of three flags: **render** (process Jinja2 syntax), **write** (emit to output), **ignore** (skip entirely). Files can be renderable without being writable, enabling logic-only includes.

### Context Merging

When overlays produce context updates, keys are merged according to `composition.merge_keys` which maps key names to strategies: `overwrite`, `nested-overwrite`, or `comprehensive` (default). `comprehensive` does intelligent recursive merging of dicts/lists.

### Pattern Resolution

`Location` models support both local filesystem paths and Git URLs. Remote patterns are cached in the platform user cache directory (via `platformdirs`). `caching.py` and `git_commands.py` manage the cache.

## Code Style

- Line length: 119 characters (ruff + black)
- Docstrings: Google style (enforced by ruff `D` rules, 90% coverage via interrogate)
- Type annotations required on all public functions (`ANN` rules; `ANN002/003/204/401` are ignored)
- Tests are in `tests/` mirroring the `project_forge/` structure

## Agent skills

### Issue tracker

Issues live in GitHub (callowayproject/project-forge), using the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Domain docs

Single-context layout — root `CONTEXT.md` + `docs/adr/`. See `docs/agents/domain.md`.
