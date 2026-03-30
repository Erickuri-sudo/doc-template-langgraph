"""Mistral OCR parser node — extracts text from PDF using Mistral OCR API."""
from __future__ import annotations
import base64
import os
from pathlib import Path

from mistralai import Mistral

from agent.state import State


def mistral_parse_pdf(state: State) -> dict:
    """Extract text from PDF using Mistral OCR API."""
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

    # Lê o PDF e converte para base64
    pdf_bytes = Path(state.pdf_path).read_bytes()
    pdf_base64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")

    # Chama o Mistral OCR
    response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{pdf_base64}",
        },
    )

    # Combina o texto de todas as páginas
    pages_text = [page.markdown for page in response.pages]
    raw_text = "\n\n".join(pages_text).strip()

    return {"raw_text": raw_text}