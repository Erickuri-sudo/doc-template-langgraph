"""Edital template generation graph."""
from __future__ import annotations

from langgraph.graph import StateGraph

from agent.state import State
from agent.nodes.pdf_parser import parse_pdf
from agent.nodes.field_extractor import extract_fields

graph = (
    StateGraph(State)
    .add_node(parse_pdf)
    .add_node(extract_fields)
    .add_edge("__start__", "parse_pdf")
    .add_edge("parse_pdf", "extract_fields")
    .compile(name="Edital Template Generator")
)