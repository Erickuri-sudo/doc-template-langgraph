import asyncio
from agent.graph import graph

result = graph.invoke({"pdf_path": "seu_edital.pdf"})

print(f"Texto extraído: {len(result['raw_text'])} caracteres")
print(result['raw_text'][:500])  # Preview dos primeiros 500 chars