#!/usr/bin/env python3
"""Export the schemas for the compositions and patterns."""
import json
from pathlib import Path

from project_forge.models.composition import Composition
from project_forge.models.pattern import Pattern


def main():
    """Export the schemas."""
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
