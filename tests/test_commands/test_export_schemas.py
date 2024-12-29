"""Tests for the export_schemas module."""

import json
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from project_forge.commands.export_schemas import export_schemas, generate_schema
from project_forge.models.composition import Composition
from project_forge.models.pattern import Pattern


class DummyModel(BaseModel):
    """Dummy model for testing."""

    name: str
    age: int


class TestGenerateSchema:
    """Tests for the generate_schema function."""

    def test_valid_model_generates_correct_schema(self):
        """Should correctly generate schema with $schema and $id fields."""
        schema = generate_schema(DummyModel)

        schema_data = json.loads(schema)
        assert schema_data["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema_data["$id"] == "https://github.com/callowayproject/project-forge/dummymodel.schema.json"
        assert "properties" in schema_data
        assert "name" in schema_data["properties"]
        assert "age" in schema_data["properties"]

    def test_empty_model_schema(self):
        """Should handle an empty model correctly."""

        class EmptyModel(BaseModel):
            pass

        schema = generate_schema(EmptyModel)

        schema_data = json.loads(schema)
        assert schema_data["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema_data["$id"] == "https://github.com/callowayproject/project-forge/emptymodel.schema.json"
        assert "properties" in schema_data
        assert not schema_data["properties"]

    def test_custom_model_name(self):
        """Should generate schema for model with specific custom class name."""

        class CustomModel(BaseModel):
            field1: str
            field2: int

        schema = generate_schema(CustomModel)

        schema_data = json.loads(schema)
        assert schema_data["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema_data["$id"] == "https://github.com/callowayproject/project-forge/custommodel.schema.json"
        assert "properties" in schema_data
        assert "field1" in schema_data["properties"]
        assert "field2" in schema_data["properties"]

    def test_invalid_model_raises_attribute_error(self):
        """Should raise an error if the input is not a valid Pydantic model."""
        mock_invalid_model = MagicMock()

        with pytest.raises(AttributeError):
            generate_schema(mock_invalid_model)


class TestExportSchemas:
    """Tests for the export_schemas function."""

    @patch("project_forge.commands.export_schemas.generate_schema")
    def test_exports_composition_schema(self, mock_generate_schema):
        """Test that generate_schema is called for the Composition model."""
        export_schemas()
        mock_generate_schema.assert_any_call(Composition)

    @patch("project_forge.commands.export_schemas.generate_schema")
    def test_exports_pattern_schema(self, mock_generate_schema):
        """Test that generate_schema is called for the Pattern model."""
        export_schemas()
        mock_generate_schema.assert_any_call(Pattern)

    @patch("project_forge.commands.export_schemas.generate_schema")
    def test_returns_schema_result(self, mock_generate_schema):
        """Test that the function returns a SchemaResult with correct schemas."""
        mock_generate_schema.side_effect = lambda model: f"schema_for_{model.__name__}"
        result = export_schemas()

        assert result.composition_schema == "schema_for_Composition"
        assert result.pattern_schema == "schema_for_Pattern"
