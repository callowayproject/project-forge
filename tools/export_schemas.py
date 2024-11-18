#!/usr/bin/env python3
"""Export the schemas for the compositions and patterns."""
import json

from project_forge.configurations.pattern import Pattern
from project_forge.configurations.composition import Composition
from pathlib import Path


def main():
    root_path = Path(__file__).parent.parent
    comp_schema_path = root_path / "composition.schema.json"
    pattern_schema_path = root_path / "pattern.schema.json"
    schema = Composition.model_json_schema()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["$id"] = "https://github.com/callowayproject/project-forge/composition.schema.json"
    comp_schema_path.write_text(json.dumps(schema, indent=2))
    schema = Pattern.model_json_schema()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["$id"] = "https://github.com/callowayproject/project-forge/pattern.schema.json"
    pattern_schema_path.write_text(json.dumps(schema, indent=2))


if __name__ == "__main__":
    main()
