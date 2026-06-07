import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_postgres import PGVector

load_dotenv(Path(__file__).parent.parent / ".env", override=True)

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def get_embeddings():
    if os.getenv("GOOGLE_API_KEY"):
        return GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001"))
    elif os.getenv("OPENAI_API_KEY"):
        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    raise ValueError("Configure GOOGLE_API_KEY ou OPENAI_API_KEY no arquivo .env")


def get_llm():
    if os.getenv("GOOGLE_API_KEY"):
        return ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_LLM_MODEL", "gemini-2.5-flash-lite"))
    elif os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(model=os.getenv("OPENAI_LLM_MODEL", "gpt-5-nano"))
    raise ValueError("Configure GOOGLE_API_KEY ou OPENAI_API_KEY no arquivo .env")


def search_prompt(question=None):
    """Inicializa o vector store e a LLM, retorna uma função que responde perguntas."""
    try:
        store = PGVector(
            embeddings=get_embeddings(),
            collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME", "desafio_collection"),
            connection=os.getenv("DATABASE_URL"),
            use_jsonb=True,
        )
        llm = get_llm()

        def answer(q):
            results = store.similarity_search_with_score(q, k=10)
            context = "\n\n".join([doc.page_content for doc, _ in results])
            prompt = PROMPT_TEMPLATE.format(contexto=context, pergunta=q)
            return llm.invoke(prompt).content

        return answer
    except Exception as e:
        print(f"Erro ao inicializar: {e}")
        return None
