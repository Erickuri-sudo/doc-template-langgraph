"""Field extractor node — identifies dynamic fields in edital text."""
from __future__ import annotations
import os
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from agent.state import State


class ExtractedField(BaseModel):
    """A single dynamic field found in the edital."""

    name: str = Field(description="Nome semântico do placeholder em SNAKE_CASE maiúsculo. Ex: VALOR_ESTIMADO")
    value: str = Field(description="Valor exato como aparece no texto do edital")
    field_type: str = Field(description="Tipo do dado: date, currency, number, string, cpf, cnpj, email, phone")
    description: str = Field(description="Descrição curta do campo em português")
    required: bool = Field(description="Se o campo é obrigatório no edital")


class ExtractedFields(BaseModel):
    """List of all dynamic fields found in the edital."""

    fields: list[ExtractedField]


SYSTEM_PROMPT = """Você é um especialista em análise de editais brasileiros.
Sua tarefa é identificar todos os campos dinâmicos em um edital — ou seja, 
informações que mudariam se este edital fosse republicado para um novo processo.

Exemplos de campos dinâmicos:
- Datas (abertura, encerramento, entrega)
- Valores financeiros (valor estimado, teto de bolsas)
- Números de processo ou edital
- Nomes de responsáveis ou coordenadores
- Prazos em dias
- Quantidades (número de vagas, bolsas)
- Órgão ou instituição responsável

NÃO considere como dinâmico:
- Texto jurídico padrão e boilerplate
- Referências a leis e decretos
- Critérios e regras fixas do processo
- Definições e conceitos

Retorne APENAS os campos que claramente variam entre editais do mesmo tipo."""


def extract_fields(state: State) -> dict[str, Any]:
    """Identify dynamic fields in the extracted edital text."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=os.environ["GOOGLE_API_KEY"],
    )

    structured_llm = llm.with_structured_output(ExtractedFields)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Analise o seguinte edital e extraia os campos dinâmicos:\n\n{state.raw_text}"),
    ]

    result: ExtractedFields = structured_llm.invoke(messages)

    return {"extracted_fields": [field.model_dump() for field in result.fields]}