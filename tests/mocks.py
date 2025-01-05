from typing import Any, Dict, Literal, Optional

from pydantic_core.core_schema import ValidationInfo


class MockValidationInfo(ValidationInfo):
    def __init__(self, context: Optional[dict] = None):
        self._context = context

    @property
    def context(self) -> Any | None:
        """Current validation context."""
        return self._context

    @property
    def config(self) -> None:
        """The CoreConfig that applies to this validation."""
        return None

    @property
    def mode(self) -> Literal["python", "json"]:
        """The type of input data we are currently validating"""
        return "python"

    @property
    def data(self) -> Dict[str, Any]:
        """The data being validated for this model."""
        return {}

    @property
    def field_name(self) -> None:
        return None
