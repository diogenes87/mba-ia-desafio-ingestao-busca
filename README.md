# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de Ingestão e Busca Semântica com LangChain e PostgreSQL + pgVector.

## Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução
- Python 3.10 ou superior
- Chave de API da **OpenAI** ou do **Google Gemini** (ao menos uma)

## Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/diogenes87/mba-ia-desafio-ingestao-busca.git
cd mba-ia-desafio-ingestao-busca
```

### 2. Crie e ative o ambiente virtual Python

```powershell
python -m venv venv
.\venv\Scripts\activate
```

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Copie o arquivo de exemplo e preencha com suas chaves:

```bash
cp .env.example .env
```

Edite o arquivo `.env` e preencha **apenas um** dos provedores de IA:

```env
# Opção A: OpenAI
OPENAI_API_KEY=sk-...
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_LLM_MODEL=gpt-5-nano

# Opção B: Google Gemini
GOOGLE_API_KEY=AIza...
GOOGLE_EMBEDDING_MODEL=models/embedding-001
GOOGLE_LLM_MODEL=gemini-2.5-flash-lite

# Banco de dados (já configurado para o Docker local)
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PG_VECTOR_COLLECTION_NAME=desafio_collection
PDF_PATH=document.pdf
```

> O sistema detecta automaticamente qual provedor usar com base na chave preenchida. Se ambas estiverem preenchidas, Google Gemini tem prioridade.

### 5. Adicione o seu PDF

Coloque o arquivo PDF na **raiz do repositório** (mesmo nível do `docker-compose.yml`) com o nome `document.pdf`:

```
mba-ia-desafio-ingestao-busca/
├── document.pdf          ← seu PDF aqui
├── docker-compose.yml
├── requirements.txt
└── src/
```

Se preferir usar um nome de arquivo diferente, atualize a variável `PDF_PATH` no `.env`:

```env
PDF_PATH=meu-relatorio.pdf
```

> **Atenção:** o PDF deve estar na raiz do repositório. Caminhos absolutos também são aceitos, ex: `PDF_PATH=C:\Users\usuario\Downloads\relatorio.pdf`

## Execução

### 1. Inicie o banco de dados

Abra o Docker Desktop e depois execute:

```bash
docker compose up -d
```

### 2. Ingira o PDF no banco vetorial

```bash
python src/ingest.py
```

Saída esperada:
```
Carregando PDF: .../document.pdf
42 chunks gerados.
Ingestão concluída: 42 chunks armazenados.
```

### 3. Inicie o chat

```bash
python src/chat.py
```

## Exemplo de uso

```
Chat iniciado. Digite 'sair' para encerrar.

Faça sua pergunta: Qual o faturamento da Empresa SuperTechIABrazil?

PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.
---

Faça sua pergunta: Quantos clientes temos em 2024?

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
---

Faça sua pergunta: sair
```

## Estrutura do projeto

```
├── docker-compose.yml        # PostgreSQL + pgVector
├── requirements.txt          # Dependências Python
├── .env.example              # Template de variáveis de ambiente
├── document.pdf              # PDF ingerido
├── src/
│   ├── ingest.py             # Ingestão do PDF no banco vetorial
│   ├── search.py             # Busca semântica + chamada à LLM
│   └── chat.py               # Interface CLI de chat
└── README.md
```

## Tecnologias

- **LangChain** — orquestração de LLM e RAG
- **PostgreSQL + pgVector** — armazenamento de vetores
- **OpenAI / Google Gemini** — embeddings e geração de respostas
- **Docker** — execução do banco de dados


## Resumo para subir a aplicação:

  Resumo dos comandos (do zero)

  # 1. Entre no diretório
  cd "<PATH_TO_REPO>\GitHub\mba-ia-desafio-ingestao-busca"

  # 2. Suba o banco (Docker Desktop deve estar aberto)
  docker compose up -d

  # 3. Ative o venv
  .\venv\Scripts\activate

  # 4. Ingira o PDF (apenas na primeira vez)
  python src/ingest.py

  # 5. Inicie o chat
  python src/chat.py

## Considerações finais
    - Sobre a versao do GEMINI foi preciso utilizar com os deltalhes abaixo para conseguir rodar localmente, essa é a versão gratis e funcional na data de hoje (2026-06-07 - YYYY-MM-DD): 
        GOOGLE_LLM_MODEL=gemini-2.5-flash-lite 
        GOOGLE_EMBEDDING_MODEL=models/gemini-embedding-001
        