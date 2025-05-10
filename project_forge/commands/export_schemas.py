#!/usr/bin/env python3
"""Export the schemas for the compositions and patterns."""

import json
from dataclasses import dataclass

from pydantic import BaseModel

from project_forge.models.composition import Composition
from project_forge.models.pattern import Pattern


@dataclass
class SchemaResult:
    """The result of exporting the schemas."""

    composition_schema: str
    pattern_schema: str


def export_schemas() -> SchemaResult:
    """Export the schemas."""
    return SchemaResult(composition_schema=generate_schema(Composition), pattern_schema=generate_schema(Pattern))


def generate_schema(model: type[BaseModel]) -> str:
    """
    Generates a JSON schema representation of a given Pydantic model.

    This function takes a Pydantic model and a schema ID to generate a JSON schema
    that adheres to the given $schema version of "https://json-schema.org/draft/2020-12/schema".
    The resulting JSON schema includes the provided schema ID.

    Args:
        model: The Pydantic model to generate the JSON schema for.

    Returns:
        A JSON string representing the schema for the provided Pydantic model.
    """
    model_name = model.__name__.lower()
    schema_id = f"https://github.com/callowayproject/project-forge/{model_name}.schema.json"
    result = model.model_json_schema()
    result["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    result["$id"] = schema_id
    return json.dumps(result, indent=2)
