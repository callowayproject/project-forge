# Changelog

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

* Initial creation
