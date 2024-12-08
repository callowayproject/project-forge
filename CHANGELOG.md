# Changelog

## 0.3.0 (2024-12-08)
[Compare the full difference.](https://github.com/callowayproject/project-forge/compare/0.2.0...0.3.0)

### Fixes

- Fixed building. [64499b6](https://github.com/callowayproject/project-forge/commit/64499b63a24336e25c7c9b68d873cca9bbb0161a)
    
- Fixed release to test pypi. [610bfa6](https://github.com/callowayproject/project-forge/commit/610bfa67b773d3323e2576a0e9c8a90dad2b5e12)
    
- Fixed tests and version preview. [241e04d](https://github.com/callowayproject/project-forge/commit/241e04daa0b79fb66a2d70654f6c2246e5623ff9)
    
- Fixed minor linting bugs. [8cad0c3](https://github.com/callowayproject/project-forge/commit/8cad0c3254e0a74a619370d43c1b19ae41f4aa8f)
    
- Fixed windows testing bug when removing a directory. [a82f645](https://github.com/callowayproject/project-forge/commit/a82f64566871fa476f79c019166de0c7698a2d0d)
    
- Fixed caching issues with uv in actions. [283590f](https://github.com/callowayproject/project-forge/commit/283590fb9aa0ee64ade78c7df290492358f13bdd)
    
- Fixed more GitHub Actions. [862197a](https://github.com/callowayproject/project-forge/commit/862197adf3be740d31d86b64c1030414561fde99)
    
- Fixed GitHub Actions. [a6733bc](https://github.com/callowayproject/project-forge/commit/a6733bc98d6a990e93e3b8540d42b1c49affc01a)
    
- Fixed coverage in GitHub Actions. [d35db77](https://github.com/callowayproject/project-forge/commit/d35db7784dea1a3fef7c7470d51b64761c839eb5)
    
- Fixed tooling and formatting. [217cfb8](https://github.com/callowayproject/project-forge/commit/217cfb8fa2e7d100d6f934f4651efbe7fa50305f)
    
### New

- Added pyproject.toml for test fixture. [91d4b1f](https://github.com/callowayproject/project-forge/commit/91d4b1f83c8edb43962acc230b36dfccd5bdb967)
    
- Added documentation configuration. [8a3c86c](https://github.com/callowayproject/project-forge/commit/8a3c86c0e1f7c56df8b72a3de1c89ea457f26e0e)
    
- Add UI function to CLI tests and refactor conftest.py. [0fbb915](https://github.com/callowayproject/project-forge/commit/0fbb915dd9ed2ab0afb37812fa6216ea65928a3d)
    
  Incorporate 'ask_question' as a UI function across CLI tests to enhance interactivity. Remove the 'inside_dir' context manager from conftest.py, streamlining the test setup by relying on pytest plugins for directory management.
- Add testing utilities and tests for Project Forge. [58b22c7](https://github.com/callowayproject/project-forge/commit/58b22c75063b9fc89fbe59e76279c11e112a1e5a)
    
  Introduce a new `project_forge.testing` module providing utilities such as `inside_dir`, `run_inside_dir`, and `use_default_ui` for testing Project Forge patterns and compositions. Additionally, implement tests for these utilities to ensure correct functionality, including context management, command execution, and handling of project creation using default settings.
### Other

- Debugging GitHub Actions. [b1a4175](https://github.com/callowayproject/project-forge/commit/b1a4175a125b1af499487f42f97bf9caac4ce179)
    
- Bump the github-actions group across 1 directory with 3 updates. [e74f7fe](https://github.com/callowayproject/project-forge/commit/e74f7fed312c6597beb5ab03aa471dcb1095b1ff)
    
  Bumps the github-actions group with 3 updates in the / directory: [actions/checkout](https://github.com/actions/checkout), [actions/setup-python](https://github.com/actions/setup-python) and [codecov/codecov-action](https://github.com/codecov/codecov-action).


  Updates `actions/checkout` from 3 to 4
  - [Release notes](https://github.com/actions/checkout/releases)
  - [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/actions/checkout/compare/v3...v4)

  Updates `actions/setup-python` from 4 to 5
  - [Release notes](https://github.com/actions/setup-python/releases)
  - [Commits](https://github.com/actions/setup-python/compare/v4...v5)

  Updates `codecov/codecov-action` from 3 to 5
  - [Release notes](https://github.com/codecov/codecov-action/releases)
  - [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/codecov/codecov-action/compare/v3...v5)

  ---
  **updated-dependencies:** - dependency-name: actions/checkout
dependency-type: direct:production
update-type: version-update:semver-major
dependency-group: github-actions


  **signed-off-by:** dependabot[bot] <support@github.com>


- [pre-commit.ci] pre-commit autoupdate. [5e87280](https://github.com/callowayproject/project-forge/commit/5e87280b5cd9260addee260048b2d910c7fcb10c)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.7.4 → v0.8.0](https://github.com/astral-sh/ruff-pre-commit/compare/v0.7.4...v0.8.0)


### Updates

- Changed the handling of paths in test yet again. [d3d35cb](https://github.com/callowayproject/project-forge/commit/d3d35cbab928b263946f18edd559272509f98494)
    
- Changed the handling of paths in test again. [5b49897](https://github.com/callowayproject/project-forge/commit/5b49897d1c079f82278fcb11e2e8cad978adbd57)
    
- Changed the handling of paths in test. [a1904ea](https://github.com/callowayproject/project-forge/commit/a1904ea5902c999bae620d4f559520c4085f7713)
    
- Refactor to use dataclass for build results. [d1fbcdd](https://github.com/callowayproject/project-forge/commit/d1fbcdd7edee1011527b3af9dc0d544b0a772fe6)
    
  Updated `build_project` function to return a `BuildResult`, now including additional UI function parameter for better flexibility. The `render_env` function now identifies and returns the project root path, enhancing build tracking.

## 0.2.0 (2024-11-18)

[Compare the full difference.](https://github.com/callowayproject/project-forge/compare/0.1.0...0.2.0)

### New

- Add test suite for CLI and enhance TODO tags. [0296f46](https://github.com/callowayproject/project-forge/commit/0296f461d77e9ada1cf1eab6a2e1fe2bbb8939ef)

  Introduced a comprehensive test suite for the CLI functionality using `pytest` and `unittest.mock.patch` to ensure robustness. Enhanced TODO tags with issue numbers for improved tracking and organization.
- Added initial CLI interface. [a6fab99](https://github.com/callowayproject/project-forge/commit/a6fab99419439d7cb64102d9755c714e27df2bda)

- Add tests and implement render functionality. [302b685](https://github.com/callowayproject/project-forge/commit/302b68590bfbe8dc3cf4faa36d71c3d0d9abfed1)

  Added two tests in `test_render.py` to verify the rendering of templates and directories. Implemented the `render_env` function in `render.py` to handle the template rendering logic. Also ensured `questions` field in the pattern configuration has a default factory list.
- Add initial documentation and assets with new CSS and images. [052af67](https://github.com/callowayproject/project-forge/commit/052af67da9f0e1cee17b8073d537ca933d1e754d)

  Created new documentation pages for tutorials, how-tos, references, and explanations. Added custom CSS files for card layouts, extra content, field lists, and mkdocstrings styling. Included new logo and favicon images.
- Add new JSON and YAML pattern files for fixture setups. [ca6df6d](https://github.com/callowayproject/project-forge/commit/ca6df6d74b1ffe4850f146aaaca7d18e64052554)

  Introduce JSON and YAML files for 'mkdocs', 'python-boilerplate', and 'python-package' fixtures. These files define template locations, questions, and extra context to streamline repository setups.
- Add URL parsing and caching capabilities to Location class. [92cbb91](https://github.com/callowayproject/project-forge/commit/92cbb91b780f44ae7633dd88b6a5e6319da848b4)

  Enhanced Location class to parse URLs, handle local file URLs, and cache parsed URLs. Updated caching functions to handle remote repository cloning and local file paths, with added tests to verify this functionality.
- Add settings configuration for project. [69ec6e9](https://github.com/callowayproject/project-forge/commit/69ec6e9e9d7a68f5c32ae0a014f4198943273f06)

  Created a new settings file (`settings.py`) to manage configurations for the project using `pydantic-settings` and `platformdirs`. Updated dependencies in `pyproject.toml` to include these new packages.
- Add unit tests and git command utility functions. [1baa00e](https://github.com/callowayproject/project-forge/commit/1baa00ecd254023f2ac07c28991174fbfef2d005)

  Implemented unit tests for various git commands in `tests/test_git_commands.py` and defined git utility functions in `project_forge/git_commands.py`. These changes ensure comprehensive coverage for git operations including repository management, branching, and applying patches.
- Add URL parsing functionality and unit tests. [d6ef3c9](https://github.com/callowayproject/project-forge/commit/d6ef3c9de350fece13ad3081ef7a4f04db319f0d)

  Introduce `project_forge.core.urls` module with functions to parse git URLs, internal paths, and path components. Additionally, provide comprehensive unit tests in `tests/test_core/test_urls.py` to validate the parsing logic.
- Add path existence and removal utility functions with tests. [cec15da](https://github.com/callowayproject/project-forge/commit/cec15da3432c1659ccebdec49acd0982a2237a55)

  Introduced `make_sure_path_exists` and `remove_single_path` functions to handle directory and file operations safely. Additionally, added tests to ensure these functions create directories if missing and remove files and directories correctly. Logging and custom error handling are also included to enhance debugging and reliability.
- Added initial composition models. [8aeda6e](https://github.com/callowayproject/project-forge/commit/8aeda6ea53589c2fea4f3d9a3e91f0bb7074232e)

- Added configuration files. [45608a5](https://github.com/callowayproject/project-forge/commit/45608a52aac67acb04422da7ce2d598a4488b07f)

### Other

- Enable default responses and fix context rendering logic. [4af116f](https://github.com/callowayproject/project-forge/commit/4af116f97bcf617751ed287378b0a3702d5df5fd)

  Simplified context rendering by directly returning non-string values and enabled forcing default responses for certain questions. This reduces unnecessary UI interactions and corrects the faulty rendering of expression values in contextual overlays.

### Updates

- Updated tooling and configuration. [a7665e6](https://github.com/callowayproject/project-forge/commit/a7665e61a89ed8b17134a66d267709ee862bbc39)

- Refactor template handling. [228c06a](https://github.com/callowayproject/project-forge/commit/228c06a1584bde05645c4af85852fdf31925aa0d)

  Refactor `catalog_templates` to incorporate directory names for better path resolution. Updated `pyproject.toml` templates to align with the new requirements structure. Added logging for template loading in the Jinja2 environment.
- Update composition tests and add context builder merge logic. [ba65296](https://github.com/callowayproject/project-forge/commit/ba6529616d11fe28ebfc57bf2ff0e4975a3294b1)

  Updated unit tests to reflect changes in overlay patterns and added merge keys in composition. Introduced new module `data_merge.py` and implemented merge strategies for combining configurations within the context builder.
- Rename and refactor `rendering` module. [9137a77](https://github.com/callowayproject/project-forge/commit/9137a77bfd825cbc9851352dfc110780ef921d55)

  Renamed `rendering.py` to `expressions.py`, and refactored to load the environment dynamically rather than using a static instance. Adjusted project to require Python 3.12 and updated dependencies accordingly, including the addition of `asttokens` and `icecream`.
- Refactor rendering module and improve template handling. [fc042a2](https://github.com/callowayproject/project-forge/commit/fc042a2e2d0b8c1e5a2378ec5290a6c824d1eb40)

  Delete `rendering.py` and establish new modular structure with `expressions.py`, `templates.py`, and `environment.py`. Update import paths accordingly and add new test cases to cover the added functionality.
- Remove debug prints and update project references. [d949cee](https://github.com/callowayproject/project-forge/commit/d949ceeacfec411873cae810536112bf8348ebcb)

  Removed unnecessary debug print statements from multiple files to clean up the codebase. Also, updated references from "cookie_composer" to "project_forge" to align with the current project's naming conventions.
- Refactor exception hierarchy in core/exceptions.py. [e2bd1d5](https://github.com/callowayproject/project-forge/commit/e2bd1d5426b30690cf3b5098d72c2c454d59b713)

  Introduce a base ProjectForgeError class and inherit all specific exceptions from it. This change enhances consistency and simplifies exception handling across Project Forge.
- Updated Ruff configuration. [4eed053](https://github.com/callowayproject/project-forge/commit/4eed053365f1a8ff1fd88e5f12a2ac98b11a21a9)

## 0.1.0 (2024-08-26)

- Initial creation
