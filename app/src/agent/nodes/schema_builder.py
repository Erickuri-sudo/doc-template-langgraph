"""Schema builder node — Builds a schema based off the extracted fields."""
from __future__ import annotations
import os
from typing import Any
from agent.state import State

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

def build_schema(state: State) -> dict:
    schema_fields = []

    for field in state.extracted_fields:
        schema_fields.append({
            "name": field["name"],
            "type": field["field_type"],
            "description": field["description"],
            "required": field["required"],
            "example": field["value"], 
        })

    return {
        "schema": {
            "fields": schema_fields
        }
    }