"""Template reconstructor node — Reconstructs the template based off the original text,
changing the extracted fields into placeholders."""

import os
import re
import json
from dataclasses import replace
from ..state import State
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI


def reconstruct_template(state: State) -> State:
    original_text: str = state.raw_text
    fields_schema: dict = state.schema

    field_map = _build_field_map(fields_schema)

    # 1ª passagem: substituição determinística por regex
    working_text, unresolved = _apply_regex_substitutions(original_text, field_map)

    # 2ª passagem: LLM apenas para campos que o regex não resolveu
    if unresolved:
        working_text = _apply_llm_substitutions(working_text, unresolved)

    validation_report = _validate_placeholders(working_text, field_map)

    return replace(
        state,
        template=working_text,
        validation_errors=validation_report,
    )


def _build_field_map(fields_schema: dict) -> dict:
    """{ "valor_no_texto": "{{PLACEHOLDER}}" }"""
    field_map = {}
    for field in fields_schema.get("fields", []):
        value = field.get("example")  # ← corrigido
        name = field.get("name")
        if value and name:
            placeholder = f"{{{{{name}}}}}"
            field_map[value] = placeholder
    return field_map


def _apply_regex_substitutions(text: str, field_map: dict) -> tuple[str, dict]:
    """Substitui valores exatos encontrados no texto."""
    unresolved = {}
    for value, placeholder in field_map.items():
        escaped = re.escape(str(value))
        new_text, count = re.subn(escaped, placeholder, text)
        if count > 0:
            text = new_text
        else:
            unresolved[value] = placeholder
    return text, unresolved


def _apply_llm_substitutions(text: str, unresolved: dict) -> str:
    """Usa LLM para campos com variações de formatação que o regex não resolveu."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=os.environ["GOOGLE_API_KEY"],
    )

    system = SystemMessage(content=(
        "Você é um editor técnico. Retorne APENAS o texto modificado, "
        "sem explicações, sem markdown, sem comentários."
    ))

    prompt = f"""No texto abaixo, localize e substitua os seguintes valores pelos seus placeholders.
Os valores podem aparecer com pequenas variações de formatação (espaços, vírgulas, formatação de data).

SUBSTITUIÇÕES A FAZER:
{json.dumps(unresolved, ensure_ascii=False, indent=2)}

TEXTO:
---
{text}
---

Retorne APENAS o texto modificado."""

    response = llm.invoke([system, HumanMessage(content=prompt)])
    return response.content.strip()


def _validate_placeholders(template_text: str, field_map: dict) -> list[str]:
    errors = []
    for value, placeholder in field_map.items():
        if placeholder not in template_text:
            errors.append(f"Placeholder não inserido: {placeholder} (valor original: '{value}')")
    return errors