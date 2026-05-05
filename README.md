# Templater de Editais

Um projeto com o intuito de diminuir o tempo e o atrito de criar editais do zero.

## Sobre o projeto

Este projeto implementa um grafo no Langgraph que visa facilitar a criação de editais através de templates gerados através de editais fornecidos anteriormente. Utiliza-se ferramentas de extração de texto provenientes dos PDF's dos editais, além de um fluxo de agentes para identificação, classificação e substituição no texto original. Ao final, retorna o JSON do schema e do template.

## Pré-requisitos

## Instalação

### 1. Clone esse repositório
```bash
git clone https://github.com/Erickuri-sudo/doc-template-langgraph.git
cd doc-template-langgraph/app
```

### 2. Crie um ambiente virtual e o ative
```bash
   python3 -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

## Configuração

### 1. Sincronize as dependências
Esse projeto usa o gerenciador de pacotes **uv**.
Rode o comando
```bash
uv sync
```
no terminal para sincronizar as dependências necessárias ao projeto.

### 2. Crie um arquivo .env
Para que o grafo rode como esperado, o seu arquivo .env deve conter
```dotenv
# Nome do projeto
LANGSMITH_PROJECT = 
# Chave API do LangSmith
LANGSMITH_API_KEY = 
# Chave API do Gemini
GOOGLE_API_KEY = 

# (Opcional) Variáveis para configuração de telemetria via LangFuse
LANGFUSE_SECRET_KEY = "sk-..."
LANGFUSE_PUBLIC_KEY = "pk-..."
LANGFUSE_BASE_URL = 
```