# Changelog

## 0.6.0 (2025-05-21)
[Compare the full difference.](https://github.com/callowayproject/project-forge/compare/0.5.1...0.6.0)

### Fixes

- Fix permissions on bump-version.yaml workflow. [5cd391d](https://github.com/callowayproject/project-forge/commit/5cd391d842e424ee7da9f0aab8d1a3eeabe518b6)
    
- Fix github release permissions. [ee5098f](https://github.com/callowayproject/project-forge/commit/ee5098f65d296c54dd4cc53a08adf4fd3083e3f8)
    
- Fix trusted publishing does not support reusable workflows. [dad426c](https://github.com/callowayproject/project-forge/commit/dad426c204281efddf03cb020b8277d097122a28)
    
- Fixed permissions in github release workflow. [9af70bf](https://github.com/callowayproject/project-forge/commit/9af70bf66588ac8cb7302beec1ff02b669ef35a4)
    
- Fixed typo in changelog. [cba3d9e](https://github.com/callowayproject/project-forge/commit/cba3d9e297af5675a7cd35c78822681a02d8e197)
    
- Fixed bad default param for release-github.yaml. [01cb923](https://github.com/callowayproject/project-forge/commit/01cb923795e7649086c9e022bd7e5381812ffcf0)
    
### New

- Add RenderError exception and handle template rendering issues. [ff8f719](https://github.com/callowayproject/project-forge/commit/ff8f719254eb7932a1a1862056fb3b9977b0be13)
    
  Introduce a `RenderError` exception to handle problems during template rendering. Update the rendering logic to raise `RenderError` when encountering `UnicodeDecodeError` or `FileNotFoundError`. This improves error handling and makes issues easier to debug.
- Add always_skip setting to configure globally skipped patterns. [7384424](https://github.com/callowayproject/project-forge/commit/7384424265e03b2b8c8e568fd92d1e00a1451376)
    
  Introduced an `always_skip` setting to define patterns that are always skipped during processing. Updated `get_settings` to cache settings and integrated `always_skip` into the `get_process_mode` logic for more flexible path matching.
### Updates

- Renamed job from release-github to call-release-github. [b1ca996](https://github.com/callowayproject/project-forge/commit/b1ca996092d8b24bf8c18e32ff0d349f9dcd0de6)
    
- Removed unused workflow: release-pypi.yaml. [b543406](https://github.com/callowayproject/project-forge/commit/b543406d3ba8ef00e2c2184776bfcc4a1d16030a)
    

## 0.5.1 (2025-05-10)

[Compare the full difference.](https://github.com/callowayproject/project-forge/compare/0.5.0...0.5.1)

### Fixes

- Fixed installation of bump-my-version. [a1b8b59](https://github.com/callowayproject/project-forge/commit/a1b8b59fd22007df550929ed5ef6bdf0c83ebd35)

- Refactor CLI to parse composition as git URL. [78282f2](https://github.com/callowayproject/project-forge/commit/78282f2523baeae3d17629a6af1f4148fd39f987)

    Updated the `composition` argument in the `build` command to accept a git URL instead of a file path. Added parsing logic to convert the URL into a file path before processing, enabling more flexible input handling.

- Refactor workflows for improved release management. [b9d119b](https://github.com/callowayproject/project-forge/commit/b9d119b7bf66db57dde852cf7f455adc5095abf1)

    Updated workflows to support passing a reference (ref) input for consistent release processes. Renamed jobs, fixed pip command, and added outputs like tag_name for improved clarity and functionality.

- Fixed permissions on release-github and release-pypi workflows. [36502b4](https://github.com/callowayproject/project-forge/commit/36502b4b9a5a3c195385a513afa2a50c7f978903)

### Other

- Reformatted the CHANGELOG.md file. [d9e9def](https://github.com/callowayproject/project-forge/commit/d9e9def463f66398360a575c673792f953dd9e44)

- Simplify workflow definition by replacing steps with "uses". [74e023a](https://github.com/callowayproject/project-forge/commit/74e023ad4ca35d4450cb0ff904c8c9474c72bf27)

    Removed explicit steps under `release-github` and `release-pypi` jobs, replacing them with direct `uses` references to corresponding workflow files.

## 0.5.0 (2025-05-10)

[Compare the full difference.](https://github.com/callowayproject/project-forge/compare/0.4.0...0.5.0)

### Fixes

- Fixed pre-commit configuration. [c78925c](https://github.com/callowayproject/project-forge/commit/c78925c10fe8a4332a60600d66c1575e749e9a20)

### Other

- Formatted the CHANGELOG.md file. [44555c3](https://github.com/callowayproject/project-forge/commit/44555c38fece334543dc45375bee1b88751d97d6)

- Bump astral-sh/setup-uv from 5 to 6 in the github-actions group. [836274b](https://github.com/callowayproject/project-forge/commit/836274b7c42a3b6335817cc84467dfd220a6ae70)

    Bumps the github-actions group with 1 update: [astral-sh/setup-uv](https://github.com/astral-sh/setup-uv).

    Updates `astral-sh/setup-uv` from 5 to 6

    - [Release notes](https://github.com/astral-sh/setup-uv/releases)
    - [Commits](https://github.com/astral-sh/setup-uv/compare/v5...v6)

    ---

    **updated-dependencies:** - dependency-name: astral-sh/setup-uv
    dependency-version: '6'
    dependency-type: direct:production
    update-type: version-update:semver-major
    dependency-group: github-actions

    **signed-off-by:** dependabot[bot] <support@github.com>

### Updates

- Refactor URL parsing to include `internal_path` handling. [edd72cc](https://github.com/callowayproject/project-forge/commit/edd72cc77563fd494c6010ef74cc33c1f95a9d78)

    Enhance the `parse_internal_path` function to handle `internal_path` and `checkout` extraction more robustly, including cases with blob paths. Update tests and related logic to reflect the new `internal_path` field support.

- Update bump-version workflow to enable package builds. [3ddd6cf](https://github.com/callowayproject/project-forge/commit/3ddd6cfc859ae0394e05323420cb8411a000ac2d)

    Changed the `build_package` output to `true` for version bumps, ensuring package building is triggered. Also added `packages: write` permission to support this new functionality.

## 0.4.0 (2025-05-07)

[Compare the full difference.](https://github.com/callowayproject/project-forge/compare/0.3.0...0.4.0)

### Fixes

- Fixed GitHub workflows. [2a3e4b7](https://github.com/callowayproject/project-forge/commit/2a3e4b7836511d575387f384c368e7ceb98c5c76)

    - build-python.yaml: removed release-container call
    - bump-version.yaml: added required permissions

- Fixed quoting test composition strings. [49aab87](https://github.com/callowayproject/project-forge/commit/49aab873e471a42b91633dd95f9138877fc70f1a)

- Fixed missing dependencies. [7a73d3e](https://github.com/callowayproject/project-forge/commit/7a73d3e17590a4c5b4336612ff640c568e3f9367)

- Fixed README. [1e61954](https://github.com/callowayproject/project-forge/commit/1e619544ccc5d8b3cd4d295b5f9ee5e495d313df)

- Fixed click docs rendering. [baf2522](https://github.com/callowayproject/project-forge/commit/baf25221dae5635b4c9448c28488da4bb3527780)

- Fixed releasing. [6f232bd](https://github.com/callowayproject/project-forge/commit/6f232bd4f73acb97b431dd543eaf85e1e172878f)

### New

- Add `run_inside_dir` and `inside_dir` utilities with tests. [3fe4460](https://github.com/callowayproject/project-forge/commit/3fe4460c968e0415e8ef510e22e63831610c137f)

    Introduced `run_inside_dir` and `inside_dir` utilities to streamline running commands within specific directories. Updated related tests to ensure proper behavior and functionality. Enhanced test coverage for `forger` fixture and adjusted naming for clarity in `return_defaults` test.

- Add new assets for branding and web app support. [0094d37](https://github.com/callowayproject/project-forge/commit/0094d37854033da244a695bf12dcd34ab0d5b5b2)

    Added dark and light logos, updated the favicon, and included a web app manifest file to support Progressive Web App features. These changes enhance branding consistency and improve app usability across platforms.

- Add utility functions for path and pattern matching. [84f637c](https://github.com/callowayproject/project-forge/commit/84f637cdd2354e12b244d58105d7217cf544ea92)

    Introduces `rel_fnmatch` to enforce relative pattern matching and `matches_any_glob` to check paths against multiple glob patterns. These functions enhance flexibility and simplify matching logic for file and path operations.

- Add support for optional skip conditions in filter_choices. [f0af00b](https://github.com/callowayproject/project-forge/commit/f0af00b5cd87b8de08ced9b94c6756ee4bc2e064)

    Previously, the `skip_when` attribute for `Choice` was mandatory, causing issues when unset. This update ensures that `skip_when` defaults to `False` if not provided, improving robustness. Additionally, a new test case was added to cover this scenario with an extra choice.

- Add issue templates for feature requests and bug reports. [4ab21e1](https://github.com/callowayproject/project-forge/commit/4ab21e18189b7d6bfacadea0797907dc3aaf9382)

    Introduced standardized GitHub issue templates to streamline project contributions. The feature request template helps users suggest ideas, while the bug report template aids in reporting issues clearly and consistently.

- Add support for tasks in composition steps. [f1afc58](https://github.com/callowayproject/project-forge/commit/f1afc580e45fc88ee3fe91cee80843cc70c7ebf1)

    Updated `composition1.toml` to include a new task step with a `git init` command. Modified the test suite to handle and validate the inclusion of tasks, ensuring correct behavior when reading composition files.

### Other

- [pre-commit.ci] pre-commit autoupdate. [56331a7](https://github.com/callowayproject/project-forge/commit/56331a72fdc0f017a6056e70cb6077f0b1cfc89d)

    **updates:** - [github.com/psf/black: 24.10.0 → 25.1.0](https://github.com/psf/black/compare/24.10.0...25.1.0)

- Create codeql.yml. [671be99](https://github.com/callowayproject/project-forge/commit/671be99aca5bd86265b77760e2444e926f41b393)

- Simplify URL existence check in \_process_url method. [a7e87fc](https://github.com/callowayproject/project-forge/commit/a7e87fcab17b63260c72497c31def9109aa7a8b9)

    Removed unnecessary use of the second argument in `dict.get` method when checking for the presence of a URL key. This change streamlines the code and improves readability without altering functionality.

- Set specific permissions for GitHub Actions workflows. [c552ada](https://github.com/callowayproject/project-forge/commit/c552ada1338f1e2c3aca6a8950a4d83e134ba318)

    Added `contents: read` and `pull-requests: write` permissions to ensure workflows have the least privilege required. This enhances security while maintaining necessary functionality.

- Potential fix for code scanning alert no. 6: Workflow does not contain permissions. [80f897f](https://github.com/callowayproject/project-forge/commit/80f897f51103c98ba9dc4bfbe5bec2eb856c6898)

    **co-authored-by:** Copilot Autofix powered by AI \<62310815+github-advanced-security[bot]@users.noreply.github.com>

- Switch changelog action to use Docker image source. [06d8bf9](https://github.com/callowayproject/project-forge/commit/06d8bf9992ee7c1b9ecf037512c0be98164f2df4)

    Updated workflows to use the Docker image source for the `callowayproject/generate-changelog` action. This ensures consistency and better alignment with repository hosting. No functional changes to workflow behavior are introduced.

- Disable GPG signing in test repository setup. [b1348b6](https://github.com/callowayproject/project-forge/commit/b1348b6c93d5fb6c72b5d41299bb60af1bdfc117)

    This ensures that GPG signing is disabled for commits and tags in test repositories, preventing unnecessary or failing GPG-related checks during testing. It improves the consistency and reliability of test environments.

- Implement skip and copy_only file handling in rendering. [2e83acf](https://github.com/callowayproject/project-forge/commit/2e83acf7b8662191f8af493051f3596805018b2d)

    Added functionality to process skip and copy_only file patterns during template rendering. Updated corresponding tests and logic in multiple modules to ensure correct skipping, copying, and rendering behavior. Improved code clarity and removed outdated TODO comments.

    Fixes #20

- [pre-commit.ci] pre-commit autoupdate. [e4da30f](https://github.com/callowayproject/project-forge/commit/e4da30f2b31179539d9b904da15675d92db0fccc)

    **updates:** - [github.com/jsh9/pydoclint: 0.5.13 → 0.5.14](https://github.com/jsh9/pydoclint/compare/0.5.13...0.5.14)

- Exclude cli.md from search results in docs. [caf433e](https://github.com/callowayproject/project-forge/commit/caf433e04906717e0686dd784616ed6766d42574)

    Updated the MkDocs configuration to exclude cli.md from search indexing. This helps streamline search results by removing irrelevant or less frequently needed content.

- "Update documentation and fix formatting inconsistencies. [b228c5c](https://github.com/callowayproject/project-forge/commit/b228c5c8205afaaf9b54ae7b900b4b78120e60da)

    Revised multiple documentation files including CODE_OF_CONDUCT.md, CONTRIBUTING.md, and ISSUE_TEMPLATE.md to address formatting issues, ensure consistent indentation, and improve clarity. Updated outdated references and added accurate contact details to enhance usability and maintain alignment with project standards."

- [pre-commit.ci] pre-commit autoupdate. [9702aef](https://github.com/callowayproject/project-forge/commit/9702aef5e7602c2c10fcfd24a0307a760f95259d)

    **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.8.2 → v0.8.4](https://github.com/astral-sh/ruff-pre-commit/compare/v0.8.2...v0.8.4)

- Use `working_dir` for task execution and implement `process_task`. [90add5e](https://github.com/callowayproject/project-forge/commit/90add5eb8d0b15affa3e19075c6a3657cb071ead)

    Updated task execution to utilize a configurable `working_dir` instead of defaulting to the output directory. Also implemented `process_task` to call `execute_task`, replacing the placeholder `NotImplementedError`.

### Updates

- Removed bumpversion replace rul for non-existent replacement. [6d49266](https://github.com/callowayproject/project-forge/commit/6d492661eacfd3af0df4ae8c3c41f06e68c41571)

- Update documentation for composition and add overlay reference. [74b125d](https://github.com/callowayproject/project-forge/commit/74b125d5c54ee57623f97c076c53658024b6d118)

    Clarified the composition file structure, including the `steps` and `merge_keys` attributes, to highlight overlay behavior and merging functionality. Enhanced the README to better explain Project Forge's extensibility and key features. Added a new `overlay.md` file to provide a dedicated reference for overlay configuration.

- Refactor GitHub Actions workflows for improved modularization. [85067ec](https://github.com/callowayproject/project-forge/commit/85067ececb073445aaa97ac11e8c46bfa4a8e090)

    Reorganized workflows into smaller, modular components for clarity and maintainability. Legacy workflows were removed, and new workflows were introduced to separate tasks such as documentation, testing, version bumping, and releases to GitHub and PyPI.

- Refactor command rendering to support context variables. [f9df4ab](https://github.com/callowayproject/project-forge/commit/f9df4abca4352e7f2db29a98d74bdc51b22f770c)

    Updated `Task` execution to render context variables in both string and list commands before execution. Added corresponding parameterized test cases to validate this behavior.

- Remove `use_defaults` parameter for cleaner UI handling. [fa55dd7](https://github.com/callowayproject/project-forge/commit/fa55dd724b25e7e6eefc7831ee650f4dddc21a9b)

    Replaced the `use_defaults` parameter with explicit use of `return_defaults` in UI function handling to streamline and simplify the build logic. Updated related tests, CLI, and core functionality to align with this refactoring.

- Refactor template processing to include process modes. [c2ab5ed](https://github.com/callowayproject/project-forge/commit/c2ab5ed12a34fbfc276748bb24d11fea549fce02)

    Updated the build process to handle template paths with associated processing modes. This change lays the groundwork for incorporating `skip` and `copy_only` attributes in a future update, as noted in TODO[#20].

- Refactor template processing to support customizable modes. [2071e02](https://github.com/callowayproject/project-forge/commit/2071e029460f75512113b073f093887514c8b48a)

    Enhanced template handling by introducing `ProcessMode` and `TemplateFile` for fine-grained control over rendering and writing. Updated functions like `catalog_templates` and `catalog_inheritance` to utilize these new constructs. Adjusted tests and core logic to align with the updated template processing flow.

- Refactor UI imports and streamline default handling. [fb8dae6](https://github.com/callowayproject/project-forge/commit/fb8dae6977427855235ecb4876e2d86ef3bd6103)

    Replaced `use_default_ui` function with `return_defaults` for simplification and unified default handling. Adjusted imports to reflect module restructuring. Improves code maintainability and aligns with updated project structure.

- Refactor UI module and improve test structure. [299517f](https://github.com/callowayproject/project-forge/commit/299517fad60c54c3acb99346aa2b05b9a3eb14ad)

    Renamed `tui.py` to `ui/terminal.py` and introduced a new `ui/defaults.py` for handling default UI behavior. Updated tests to reflect these changes, including restructuring test files and replacing `tui` references with `ui.terminal` or `ui.defaults` as appropriate. This organizes the UI logic and testing structure for better clarity and maintainability.

- Refactor overlay processing to improve context merging. [a86a74d](https://github.com/callowayproject/project-forge/commit/a86a74dcdb8ef30563fe50f1a3a8291c335d112b)

    Replaced mock UI with `return_defaults` and updated tests accordingly. Enhanced the `process_overlay` return logic to re-merge the pattern context, ensuring extra context requiring answers is properly rendered. Simplified and clarified related test cases.

- Updated feature request template. [45827f7](https://github.com/callowayproject/project-forge/commit/45827f7d28389daa802bdb8d1f0acb7621660f3f)

- Refactor schema export and improve composition handling. [b4989f1](https://github.com/callowayproject/project-forge/commit/b4989f180cefb039adfb33294b486c84ba7c28cb)

    Replaced the standalone `export_schemas.py` script with a more structured `export_schemas` command in the CLI. Added support for tasks alongside overlays within compositions and introduced relevant JSON schema updates. Comprehensive tests were added to ensure reliable schema generation and export functionality.

- Update documentation formatting. [f920794](https://github.com/callowayproject/project-forge/commit/f920794ffc24738082cecbf651feab1c92e7bd12)

- Update docs with generation of Click docs. [2b99189](https://github.com/callowayproject/project-forge/commit/2b99189dd918f661a761ec9e288f07b28d6a3de9)

- Update documentation and improve reference links. [7d48f18](https://github.com/callowayproject/project-forge/commit/7d48f18b709ff445d614830203b3db7f85b1c40c)

    Refactored documentation to correct and update API references from `configurations` to `models` for accuracy. Introduced a new CLI documentation file and adjusted formatting in tutorials for better readability. Added HTML comment markers in `README.md` for improved structure.

- Refactor tests to improve composition mocking and assertions. [c9d6587](https://github.com/callowayproject/project-forge/commit/c9d6587b0f5980d216650c37f837b03f8cc20c6c)

    Simplified test setup by creating helper methods for mock composition creation and setting return values. Enhanced readability and maintainability by replacing repetitive mock assertions with a shared utility method. Added coverage for `process_task` functionality, ensuring all patches are handled consistently.

- Refactor configuration models and adjust related modules. [a493bc8](https://github.com/callowayproject/project-forge/commit/a493bc8abd77caa472d5bf54a307f76996c3796e)

    Moved configuration-related logic into dedicated "models" module, splitting classes like Overlay into their own files. Updated references across the project to reflect this restructuring, improving maintainability and separation of concerns.

- Updated readme. [64dc91e](https://github.com/callowayproject/project-forge/commit/64dc91ede59a57cdfceba768655e4019450c9cfb)

- Updated docs. [df2de03](https://github.com/callowayproject/project-forge/commit/df2de03733ddb0126ede8d7a8421d70ef3191b40)

- Updated tools. [b817479](https://github.com/callowayproject/project-forge/commit/b817479515902e3176c4e6060f7f1bfe9bdca51b)

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
