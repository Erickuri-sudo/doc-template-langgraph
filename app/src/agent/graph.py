"""Edital template generation graph."""
from __future__ import annotations

from langgraph.graph import StateGraph
from langfuse.langchain import CallbackHandler

from agent.state import State
from agent.nodes.pdf_parser import parse_pdf
from agent.nodes.field_extractor import extract_fields
from agent.nodes.export_schema import export_schema_to_json
from agent.nodes.schema_builder import build_schema
from dotenv import load_dotenv

load_dotenv()
langfuse_handler = CallbackHandler()    


graph = (
    StateGraph(State)
    .add_node(parse_pdf)
    .add_node(extract_fields)
    .add_node(build_schema)
    .add_node(export_schema_to_json)
    .add_edge("__start__", "parse_pdf")
    .add_edge("parse_pdf", "extract_fields")
    .add_edge("extract_fields","build_schema")
    .add_edge("build_schema","export_schema_to_json")
    .add_edge("export_schema_to_json","__end__")
    .compile(name="Edital Template Generator")
    .with_config({"callbacks": [langfuse_handler]})

)
