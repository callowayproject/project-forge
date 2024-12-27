---
title: Reference
summary: Technical reference of Project Forge.
date: 2024-08-26
---

# Reference

- **Location.** A location is a reference to a source.
- **Pattern.** A set of template files to render and a rendering configuration file.
- **Pattern source management.** Downloading and caching the pattern sources (git repos, local directories)
- **Overlay.** A reference to a pattern and the configuration for using it in a specific composition.
- **Composition.** A list of overlays and context to render a project.
- **Template Rendering Engine.** The system that defines the structure of the templates and renders them into the final product
- **Tasks.** Commands that are run during the generation process.
- **Context.** The set of values that the *template rendering engine* uses to render templates
- **Question management.** Manages the questions across multiple overlays in a composition. Handles actual validation (Passes UI a validation function for each question)
- **User input.** Manages the questioning, validation, and error handling of user input for the pattern questions.
- **Migrations.** Adding overlays and updating overlays on projects
