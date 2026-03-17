"""Edital template generation graph."""
from __future__ import annotations

from langgraph.graph import StateGraph

from agent.state import State
from agent.nodes.pdf_parser import parse_pdf

graph = (
    StateGraph(State)
    .add_node(parse_pdf)
    .add_edge("__start__", "parse_pdf")
    .compile(name="Edital Template Generator")
)