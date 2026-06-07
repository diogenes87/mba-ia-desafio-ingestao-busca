import os
import time
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv(Path(__file__).parent.parent / ".env", override=True)


class GeminiEmbeddingsWithDelay(GoogleGenerativeAIEmbeddings):
    """Usa embed_query individualmente para evitar limites do batchEmbedContents."""
    def embed_documents(self, texts):
        results = []
        for i, text in enumerate(texts):
            results.append(self.embed_query(text))
            if (i + 1) % 5 == 0 and i + 1 < len(texts):
                time.sleep(1)
        return results


def get_embeddings():
    if os.getenv("GOOGLE_API_KEY"):
        return GeminiEmbeddingsWithDelay(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/gemini-embedding-001"))
    elif os.getenv("OPENAI_API_KEY"):
        return OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    raise ValueError("Configure GOOGLE_API_KEY ou OPENAI_API_KEY no arquivo .env")


def ingest_pdf():
    pdf_path_env = os.getenv("PDF_PATH", "document.pdf")
    pdf_path = Path(pdf_path_env)
    if not pdf_path.is_absolute():
        pdf_path = Path(__file__).parent.parent / pdf_path_env

    print(f"Carregando PDF: {pdf_path}")
    docs = PyPDFLoader(str(pdf_path)).load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)
    print(f"{len(chunks)} chunks gerados. Iniciando ingestão...")

    store = PGVector(
        embeddings=get_embeddings(),
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME", "desafio_collection"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )
    store.add_documents(documents=chunks)
    print(f"Ingestão concluída: {len(chunks)} chunks armazenados.")


if __name__ == "__main__":
    ingest_pdf()
