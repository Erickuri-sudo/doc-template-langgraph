"""State definition for the edital processing graph."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class State:
    """State shared across all nodes in the graph.
    
    Attributes:
        pdf_path: Local path to the PDF file (for testing).
        raw_text: Extracted text from the edital body (up to annexes).
        extracted_fields: List of dynamic fields found in the edital.
        schema: JSON Schema of the placeholders.
        template: Rewritten edital with placeholders.
        validation_errors: Errors found during validation.
        iteration_count: Number of extraction retry iterations.
    """
    pdf_path: str = ""
    raw_text: str = ""
    extracted_fields: list[dict[str, Any]] = field(default_factory=list)
    schema: dict[str, Any] = field(default_factory=dict)
    template: str = ""
    validation_errors: list[str] = field(default_factory=list)
    iteration_count: int = 0