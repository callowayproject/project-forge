# Questions

- Treats everything as a composition.
- Resolves the dependency tree for questions across all overlays
- Uses the *User Interface* to ask questions and updates context and dependencies
- Output is a single context used to render all templates
- Handles validation
    - Can pass validation function for each question to user interface
- Interface:
    - `Pattern` or `Composition`
    - `UI` (reference)
