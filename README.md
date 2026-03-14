# AI Government Scheme Interpreter 🇮🇳

Production-ready project scaffold for a RAG system that explains Indian government scheme PDFs in simple language and translates responses into Hindi, Kannada, Tamil, and Telugu.

## Generated framework

```text
frontend/
backend/
rag/
vector_db/
database/
utils/
docs/
scripts/
```

## Quick start

### 1) Backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
cd backend
uvicorn app.main:app --reload
```

### 2) Frontend
```bash
cd frontend
npm install
npm run dev
```

## Minimal implemented endpoints

- `POST /api/v1/documents/upload`: Uploads PDF, parses/chunks text, embeds and stores in ChromaDB.
- `POST /api/v1/query/ask`: Retrieves context via vector search, builds LangChain prompt, generates answer, and translates output.

## Architecture source

Detailed architecture and roadmap are documented in:
- `docs/system-architecture-and-development-plan.md`
