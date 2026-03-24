"""PDF parser node — extracts text from edital body, stopping before annexes."""
from __future__ import annotations
import pdfplumber
import re
from agent.state import State
'''
CUTOFF_PATTERNS = [
    r"^\d+\.\s*ANEXOS?\b",        # "15. ANEXOS" ou "15. ANEXO"
    r"^ANEXO\s+[IVX\d]+\b",       # "ANEXO I", "ANEXO 1"
    r"^APÊNDICE\s+[IVX\d]+\b",    # "APÊNDICE A"
    r"^DOS\s+ANEXOS\b",           # "DOS ANEXOS"
]
'''

CUTOFF_PATTERNS = [
    r"^\d+\.\s*ANEXOS?\s*$",           # "15. ANEXOS" — linha só com isso
    r"^ANEXO\s+[IVX\d]+\s*$",          # "ANEXO I" — linha só com isso
    r"^APÊNDICE\s+[IVX\d]+\s*$",       # "APÊNDICE A" — linha só com isso
    r"^DOS\s+ANEXOS\s*$",              # "DOS ANEXOS" — linha só com isso
]


FOOTER_PATTERNS = [
    r"Funda[çc][aã]o de Amparo",
    r"Tel[:.]?\s*\d",
    r"editais\.duvidas@",
    r"fapes\.es\.gov\.br",
]


def parse_pdf(state: State) -> dict:
    """Extract text from PDF up to the first annex marker."""
    extracted_pages: list[str] = []

    with pdfplumber.open(state.pdf_path) as pdf:
        for page in pdf.pages:
            page_text = extract_page_text(page)
            page_text = _remove_footer(page_text)        # <- novo
            before_annex, found_marker = _split_at_annex(page_text)  # <- novo

            if before_annex.strip():
                extracted_pages.append(before_annex)

            if found_marker:
                break

    raw_text = "\n\n".join(extracted_pages).strip()
    return {"raw_text": raw_text}


def extract_page_text(page) -> str:
    """Extract only horizontally-oriented text from page."""
    words = page.extract_words()
    horizontal_words = [
        w for w in words
        if abs(w.get("upright", 1)) > 0.5
    ]

    if not horizontal_words:
        return page.extract_text() or ""

    sorted_words = sorted(horizontal_words, key=lambda w: (round(w["top"], 1), w["x0"]))
    lines: list[str] = []
    current_line: list[str] = []
    current_top = None

    for word in sorted_words:
        top = round(word["top"], 1)
        if current_top is None or abs(top - current_top) > 3:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word["text"]]
            current_top = top
        else:
            current_line.append(word["text"])

    if current_line:
        lines.append(" ".join(current_line))

    return "\n".join(lines)


def _remove_footer(text: str) -> str:
    """Remove repeating footer lines from page text."""
    lines = text.splitlines()
    clean_lines = [
        line for line in lines
        if not any(re.search(p, line, re.IGNORECASE) for p in FOOTER_PATTERNS)
    ]
    return "\n".join(clean_lines)


def _split_at_annex(text: str) -> tuple[str, bool]:
    """Split page text at annex marker, returning content before it."""
    lines = text.splitlines()
    clean_lines = []

    for line in lines:
        normalized = line.strip().upper()
        for pattern in CUTOFF_PATTERNS:
            if re.match(pattern, normalized):
                return "\n".join(clean_lines), True
        clean_lines.append(line)

    return "\n".join(clean_lines), False


def _is_annex_page(text: str) -> bool:
    """Return True only if an annex section header is found at line start."""
    for line in text.splitlines():
        normalized = line.strip().upper()
        for pattern in CUTOFF_PATTERNS:
            if re.match(pattern, normalized):
                return True
    return False