import json
import os
from agent.state import State

def export_schema_to_json(state: State) -> dict:
    """
    Converte o schema para JSON, salva em um arquivo físico 
    e atualiza o estado do grafo.
    """
    
    schema_dict = state.schema
    
    if not schema_dict:
        return {"schema_json": "{}"}

    # 1. Gerar a string JSON formatada
    schema_as_json_string = json.dumps(schema_dict, indent=4, ensure_ascii=False)

    # 2. Definir o nome e caminho do arquivo
    # Você pode usar um nome fixo ou algo dinâmico vindo do state
    file_name = "schema_extraido.json"
    
    # 3. Criar e escrever o arquivo no disco
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(schema_as_json_string)
        print(f"✅ Arquivo {file_name} criado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")

    # 4. Retornar para o LangGraph atualizar o State
    return {
        "schema_json": schema_as_json_string
    }