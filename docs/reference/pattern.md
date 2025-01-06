# Pattern

[Patterns](api/project_forge/models/pattern.md#project_forge.models.pattern.Pattern) are meant to be focused and reusable chunks of templated content. Although patterns are renderable as-is, you may combine patterns using a *composition.*

A [pattern](api/project_forge/models/pattern.md#project_forge.models.pattern.Pattern) consists of a set of template files and a configuration file.

## Pattern configuration

The configuration file defines the context required to render the template and the rendering rules.

You may use YAML, JSON, or TOML formatting to define the configuration.

=== "TOML"

    ```toml
    template_location = "{{ repo_name }}"
    copy_only = [
      "overrides/**/*",
      "overrides/**/.*",
    ]

    [[questions]]
    name = "project_name"
    prompt = "What is the human-friendly name of the project?"
    type = "str"
    default = "My Project"

    [[questions]]
    name = "package_name"
    prompt = "What is the name of the Python package?"
    type = "str"
    default = "{{ project_name|lower|replace(' ', '_') }}"

    [[questions]]
    name = "repo_name"
    prompt = "What is the name of the project repository?"
    type = "str"
    default = "{{ package_name|replace('_', '-') }}"

    [[questions]]
    name = "project_description"
    help = "A sentence or two about what this project does."
    type = "str"
    default = ""

    [extra_context.requirements]
    docs = [
      "black",
      "markdown-customblocks",
      "mdx-truly-sane-lists",
      "mkdocs",
      "mkdocs-click",
      "mkdocs-gen-files",
      "mkdocs-git-authors-plugin",
      "mkdocs-git-committers-plugin",
      "mkdocs-git-revision-date-localized-plugin",
      "mkdocs-include-markdown-plugin",
      "mkdocs-literate-nav",
      "mkdocs-material",
      "mkdocs-section-index",
      "mkdocstrings[python]",
      "python-frontmatter",
    ]
    ```

=== "JSON"

    ```json
    {
      "template_location": "{{ repo_name }}",
      "copy_only": [
        "overrides/**/*",
        "overrides/**/.*"
      ],
      "questions": [
        {
          "name": "project_name",
          "prompt": "What is the human-friendly name of the project?",
          "type": "str",
          "default": "My Project"
        },
        {
          "name": "package_name",
          "prompt": "What is the name of the Python package?",
          "type": "str",
          "default": "{{ project_name|lower|replace(' ', '_') }}"
        },
        {
          "name": "repo_name",
          "prompt": "What is the name of the project repository?",
          "type": "str",
          "default": "{{ package_name|replace('_', '-') }}"
        },
        {
          "name": "project_description",
          "help": "A sentence or two about what this project does.",
          "type": "str",
          "default": ""
        }
      ],
      "extra_context": {
        "requirements": {
          "docs": [
            "black",
            "markdown-customblocks",
            "mdx-truly-sane-lists",
            "mkdocs",
            "mkdocs-click",
            "mkdocs-gen-files",
            "mkdocs-git-authors-plugin",
            "mkdocs-git-committers-plugin",
            "mkdocs-git-revision-date-localized-plugin",
            "mkdocs-include-markdown-plugin",
            "mkdocs-literate-nav",
            "mkdocs-material",
            "mkdocs-section-index",
            "mkdocstrings[python]",
            "python-frontmatter"
          ]
        }
      }
    }
    ```

=== "YAML"

    ```yaml
    template_location: '{{ repo_name }}'
    copy_only:
      - overrides/**/*
      - overrides/**/.*
    questions:
      - default: My Project
        name: project_name
        prompt: What is the human-friendly name of the project?
        type: str
      - default: "{{ project_name|lower|replace(' ', '_') }}"
        name: package_name
        prompt: What is the name of the Python package?
        type: str
      - default: "{{ package_name|replace('_', '-') }}"
        name: repo_name
        prompt: What is the name of the project repository?
        type: str
      - default: ''
        help: A sentence or two about what this project does.
        name: project_description
        type: str
    extra_context:
      requirements:
        docs:
          - black
          - markdown-customblocks
          - mdx-truly-sane-lists
          - mkdocs
          - mkdocs-click
          - mkdocs-gen-files
          - mkdocs-git-authors-plugin
          - mkdocs-git-committers-plugin
          - mkdocs-git-revision-date-localized-plugin
          - mkdocs-include-markdown-plugin
          - mkdocs-literate-nav
          - mkdocs-material
          - mkdocs-section-index
          - mkdocstrings[python]
          - python-frontmatter
    ```

Includes:

- Pattern settings
- Question objects
- Choice objects

## Pattern Templates

- how context is presented
- default behavior is to render each template file in the pattern and save the results to the destination.
- Template files that match a path or glob pattern in the `skip` attribute are available for inclusion in other templates, but are not rendered individually or saved to the destination
- Template files that match a path or glob pattern in the `copy_only` attribute are not rendered. Their contents are copied to the destination

## Pattern source manager

- Contains the interface for accessing local copies of the pattern templates
- Caching logic
    - Local checkouts for remote repositories
- Hashing sources to detect changes

### Sources of patterns

- Local directory
    - For local Git repositories, we will need to deal with the potential of a dirty repo and how that affects the snapshot
        - Treat it as a Non-Git repository
        - Don't allow dirty repositories: raise an error
    - Non-Git directories
        - Hash the contents of the directory.
        - Treat it as "always new".
