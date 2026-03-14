# AI Government Scheme Interpreter 🇮🇳

## 1) System architecture diagram explanation

### High-level architecture (logical flow)

```text
[User Browser - Next.js App]
    |
    | HTTPS (JWT / session)
    v
[Nginx Reverse Proxy]
    |-------------------------------|
    v                               v
[FastAPI Backend]              [Static Frontend Assets]
    |
    |--(1) Upload PDF------------------------------>
    |     [Document Processing Service]
    |       - PyPDF / Unstructured parsing
    |       - chunking + metadata extraction
    |       - language + section tagging
    |       - store source text in PostgreSQL
    |       - generate embeddings (SentenceTransformers)
    |       - index vectors in ChromaDB (FAISS optional)
    |
    |--(2) Ask question---------------------------------------------->
    |     [RAG Orchestrator - LangChain]
    |       - query rewrite / normalization
    |       - semantic retrieval from vector DB
    |       - metadata filtering (scheme, section, state, year)
    |       - context assembly + citations
    |       - answer generation via Sarvam AI LLM
    |       - eligibility reasoning template
    |       - optional translation via Sarvam AI
    |
    |--(3) Cache hot requests/responses in Redis
    |
    |--(4) Persist users, docs, chats, audit logs in PostgreSQL
    |
    v
[JSON response: answer + confidence + citations + translations]
```

### Runtime responsibilities

- **Next.js frontend**: authentication, document upload UI, chat/Q&A interface, multilingual output toggles.
- **FastAPI backend**: API gateway, orchestration, validation, auth, rate limits, tenant isolation.
- **Document processing worker**: async extraction and chunk/embedding indexing.
- **RAG service**: retriever + prompt templates + response post-processing.
- **Sarvam AI**: answer generation and multilingual translation.
- **ChromaDB/FAISS**: fast semantic nearest-neighbor retrieval.
- **PostgreSQL**: source of truth for users/documents/chats/eligibility sessions.
- **Redis**: queue + caching for repeated user questions and translation outputs.
- **Docker + GitHub Actions**: reproducible dev/prod and CI/CD.

---

## 2) Complete folder structure

```text
ai-government-scheme-interpreter/
├─ frontend/                                  # Next.js + React + Tailwind
│  ├─ public/
│  │  ├─ locales/
│  │  │  ├─ en.json
│  │  │  ├─ hi.json
│  │  │  ├─ kn.json
│  │  │  ├─ ta.json
│  │  │  └─ te.json
│  ├─ src/
│  │  ├─ app/
│  │  │  ├─ (auth)/
│  │  │  │  ├─ login/page.tsx
│  │  │  │  └─ register/page.tsx
│  │  │  ├─ dashboard/page.tsx
│  │  │  ├─ schemes/[schemeId]/page.tsx
│  │  │  ├─ chat/[sessionId]/page.tsx
│  │  │  └─ api/health/route.ts
│  │  ├─ components/
│  │  │  ├─ upload/PdfUploader.tsx
│  │  │  ├─ chat/ChatWindow.tsx
│  │  │  ├─ chat/MessageBubble.tsx
│  │  │  ├─ eligibility/EligibilityCard.tsx
│  │  │  ├─ citations/CitationPanel.tsx
│  │  │  ├─ language/LanguageSwitcher.tsx
│  │  │  └─ common/{Button,Modal,Loader}.tsx
│  │  ├─ services/
│  │  │  ├─ apiClient.ts
│  │  │  ├─ uploadService.ts
│  │  │  ├─ chatService.ts
│  │  │  └─ translationService.ts
│  │  ├─ hooks/
│  │  │  ├─ useUpload.ts
│  │  │  ├─ useChat.ts
│  │  │  └─ useLanguage.ts
│  │  ├─ store/
│  │  │  ├─ authStore.ts
│  │  │  ├─ chatStore.ts
│  │  │  └─ uiStore.ts
│  │  ├─ types/
│  │  │  ├─ api.ts
│  │  │  ├─ scheme.ts
│  │  │  └─ chat.ts
│  │  └─ styles/globals.css
│  ├─ tailwind.config.ts
│  ├─ next.config.js
│  ├─ package.json
│  └─ Dockerfile
│
├─ backend/                                   # FastAPI app
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ core/
│  │  │  ├─ config.py
│  │  │  ├─ security.py
│  │  │  ├─ logging.py
│  │  │  └─ dependencies.py
│  │  ├─ api/
│  │  │  ├─ v1/
│  │  │  │  ├─ routes_auth.py
│  │  │  │  ├─ routes_documents.py
│  │  │  │  ├─ routes_query.py
│  │  │  │  ├─ routes_translation.py
│  │  │  │  ├─ routes_chat.py
│  │  │  │  └─ routes_admin.py
│  │  ├─ schemas/
│  │  │  ├─ auth.py
│  │  │  ├─ document.py
│  │  │  ├─ query.py
│  │  │  ├─ translation.py
│  │  │  └─ chat.py
│  │  ├─ models/
│  │  │  ├─ user.py
│  │  │  ├─ scheme_document.py
│  │  │  ├─ document_chunk.py
│  │  │  ├─ chat_session.py
│  │  │  ├─ chat_message.py
│  │  │  └─ audit_log.py
│  │  ├─ services/
│  │  │  ├─ ingestion_service.py
│  │  │  ├─ rag_service.py
│  │  │  ├─ eligibility_service.py
│  │  │  ├─ translation_service.py
│  │  │  ├─ vector_store_service.py
│  │  │  ├─ embedding_service.py
│  │  │  └─ cache_service.py
│  │  ├─ db/
│  │  │  ├─ session.py
│  │  │  ├─ base.py
│  │  │  └─ migrations/
│  │  ├─ workers/
│  │  │  ├─ celery_app.py
│  │  │  └─ tasks_ingestion.py
│  │  └─ utils/
│  │     ├─ chunking.py
│  │     ├─ prompt_templates.py
│  │     └─ language_map.py
│  ├─ tests/
│  │  ├─ test_documents_api.py
│  │  ├─ test_query_api.py
│  │  ├─ test_translation_api.py
│  │  └─ test_rag_service.py
│  ├─ requirements.txt
│  └─ Dockerfile
│
├─ infra/
│  ├─ docker-compose.yml
│  ├─ nginx/
│  │  └─ default.conf
│  ├─ postgres/
│  │  └─ init.sql
│  └─ monitoring/
│     ├─ prometheus.yml
│     └─ grafana-dashboard.json
│
├─ .github/
│  └─ workflows/
│     ├─ ci.yml
│     ├─ cd.yml
│     └─ security-scan.yml
│
├─ docs/
│  ├─ api-spec.md
│  ├─ architecture-decision-records/
│  ├─ prompt-library.md
│  ├─ system-architecture-and-development-plan.md
│  └─ onboarding.md
│
├─ scripts/
│  ├─ bootstrap.sh
│  ├─ seed_sample_schemes.py
│  └─ reindex_vectors.py
│
├─ .env.example
├─ README.md
└─ Makefile
```

---

## 3) RAG pipeline design

### Pipeline stages

1. **Upload & registration**
   - User uploads PDF with metadata (scheme name, year, language, state).
   - Save file to object storage/local volume; create `scheme_documents` row.

2. **Document parsing**
   - Parse using PyPDF first; fallback to Unstructured for noisy scans.
   - Extract page-level text, headings, tables.
   - Normalize unicode, remove boilerplate headers/footers.

3. **Chunking strategy**
   - Semantic chunking with heading-aware boundaries.
   - Target chunk size: 400–700 tokens; overlap: 80–120 tokens.
   - Attach metadata: page number, section title, scheme code, source file hash.

4. **Embedding & indexing**
   - Use SentenceTransformers model (multilingual compatible).
   - Store vectors in ChromaDB collection per scheme version.
   - Optional FAISS for high-scale or offline local indexes.

5. **Query understanding**
   - Detect query language and intent (`eligibility`, `benefits`, `documents required`).
   - Expand query with synonym templates (e.g., annual income ↔ yearly income).

6. **Retrieval**
   - Top-k vector search (k=8 default) with metadata filters.
   - Rerank to top-4 context chunks (semantic + keyword hybrid score).

7. **Generation**
   - LangChain prompt includes:
     - user question
     - retrieved context snippets + citations
     - strict instruction: “If unknown, say not found in document.”
     - plain-language style guide for Indian citizens
   - LLM: Sarvam AI completion endpoint.

8. **Eligibility reasoning layer**
   - Structured extractor identifies key conditions (income threshold, age, category, location).
   - Rule formatter generates final output:
     - **Likely Eligible / Possibly Eligible / Not Eligible / Insufficient Data**
     - concise rationale
     - required next documents

9. **Translation**
   - Generate base answer in English for consistency.
   - Translate to Hindi/Kannada/Tamil/Telugu via Sarvam AI translation API.
   - Preserve proper nouns and numeric thresholds.

10. **Response packaging**
   - Return answer + citations + confidence + translations + follow-up questions.

### RAG quality controls

- Confidence score from retrieval similarity + model self-check.
- Hallucination guard: reject answers lacking supporting citations.
- Prompt/response audit logging for traceability.
- Offline evaluation set with expected answers per scheme.

---

## 4) Backend API design (FastAPI)

### Auth APIs

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `GET /api/v1/auth/me`

### Document APIs

- `POST /api/v1/documents/upload`
  - multipart: `file`, `scheme_name`, `scheme_year`, `state`
- `GET /api/v1/documents`
- `GET /api/v1/documents/{document_id}`
- `POST /api/v1/documents/{document_id}/reindex`
- `DELETE /api/v1/documents/{document_id}`

### Query / RAG APIs

- `POST /api/v1/query/ask`
  - body:
    ```json
    {
      "document_id": "uuid",
      "question": "Am I eligible if my income is 4 lakh?",
      "preferred_language": "en",
      "target_languages": ["hi", "kn", "ta", "te"]
    }
    ```
  - response:
    ```json
    {
      "status": "success",
      "eligibility": "Possibly Eligible",
      "answer": "Based on PMAY section 4...",
      "citations": [{"page": 12, "section": "Eligibility", "snippet": "..."}],
      "confidence": 0.82,
      "translations": {
        "hi": "...",
        "kn": "...",
        "ta": "...",
        "te": "..."
      },
      "follow_up": ["Do you own a pucca house?"]
    }
    ```

### Translation APIs

- `POST /api/v1/translation/text`
- `POST /api/v1/translation/batch`

### Chat/session APIs

- `POST /api/v1/chat/sessions`
- `GET /api/v1/chat/sessions/{session_id}`
- `GET /api/v1/chat/sessions/{session_id}/messages`

### Admin/ops APIs

- `GET /api/v1/admin/health`
- `GET /api/v1/admin/metrics`
- `GET /api/v1/admin/jobs`

---

## 5) Frontend component structure

### Core pages

- **Dashboard**: uploaded schemes, status (processing/ready), quick ask.
- **Scheme detail**: document metadata, parsing health, chunk stats.
- **Chat page**: conversational eligibility Q&A with source citations.

### Key components

- `PdfUploader`
  - drag-and-drop upload, progress bar, parsing state polling.
- `ChatWindow`
  - message list + ask box + loading indicators.
- `EligibilityCard`
  - highlights verdict, confidence, and rationale summary.
- `CitationPanel`
  - shows page number + section + snippet from source PDF.
- `LanguageSwitcher`
  - toggle output language between en/hi/kn/ta/te.

### State management

- `authStore`: user profile + tokens.
- `chatStore`: sessions, messages, loading states.
- `uiStore`: selected document, language preference, notifications.

---

## 6) Required dependencies

### Frontend (Next.js)

- `next`, `react`, `react-dom`
- `tailwindcss`, `postcss`, `autoprefixer`
- `axios`
- `zustand` (or Redux Toolkit)
- `react-hook-form`, `zod`
- `i18next`, `react-i18next`
- `@tanstack/react-query`

### Backend (FastAPI)

- `fastapi`, `uvicorn[standard]`
- `pydantic`, `pydantic-settings`
- `sqlalchemy`, `psycopg2-binary`, `alembic`
- `python-multipart`
- `redis`, `celery`
- `langchain`
- `chromadb`, `faiss-cpu` (optional)
- `sentence-transformers`, `torch`
- `pypdf`, `unstructured`
- `httpx`
- `python-jose[cryptography]`, `passlib[bcrypt]`
- `prometheus-client`, `structlog`
- `pytest`, `pytest-asyncio`, `httpx` (test client)

### DevOps / Infra

- Docker, Docker Compose
- Nginx
- GitHub Actions runners
- Optional: Prometheus + Grafana

---

## 7) Database schema (PostgreSQL)

### `users`
- `id (uuid, pk)`
- `email (unique)`
- `password_hash`
- `full_name`
- `preferred_language`
- `role` (`user`/`admin`)
- `created_at`, `updated_at`

### `scheme_documents`
- `id (uuid, pk)`
- `uploaded_by (fk -> users.id)`
- `scheme_name`
- `scheme_code`
- `scheme_year`
- `state`
- `source_language`
- `file_path`
- `file_hash`
- `processing_status` (`queued`/`processing`/`ready`/`failed`)
- `total_pages`
- `created_at`, `updated_at`

### `document_chunks`
- `id (uuid, pk)`
- `document_id (fk -> scheme_documents.id)`
- `chunk_index`
- `page_number`
- `section_title`
- `content`
- `token_count`
- `embedding_id` (vector store reference)
- `created_at`

### `chat_sessions`
- `id (uuid, pk)`
- `user_id (fk -> users.id)`
- `document_id (fk -> scheme_documents.id)`
- `title`
- `created_at`, `updated_at`

### `chat_messages`
- `id (uuid, pk)`
- `session_id (fk -> chat_sessions.id)`
- `role` (`user`/`assistant`/`system`)
- `message_text`
- `language`
- `citations_json`
- `confidence_score`
- `created_at`

### `query_audit_logs`
- `id (uuid, pk)`
- `user_id (fk -> users.id)`
- `document_id (fk -> scheme_documents.id)`
- `question_text`
- `retrieved_chunk_ids`
- `model_name`
- `latency_ms`
- `status`
- `created_at`

### Indexes
- `idx_scheme_documents_status`
- `idx_document_chunks_document_page`
- `idx_chat_messages_session_created`
- `idx_query_audit_logs_doc_created`

---

## 8) Development roadmap

### Phase 0: Foundation (Week 1)
- Finalize requirements, threat model, and architecture ADRs.
- Setup monorepo, coding standards, branch rules, CI skeleton.

### Phase 1: Core ingestion + storage (Weeks 2–3)
- PDF upload API + storage.
- Parsing/chunking pipeline.
- Embedding generation + Chroma indexing.
- DB schema + migrations.

### Phase 2: RAG Q&A MVP (Weeks 4–5)
- Query endpoint + retriever + Sarvam response generation.
- Citations and confidence scoring.
- Basic frontend upload + ask interface.

### Phase 3: Multilingual and eligibility logic (Weeks 6–7)
- Translation to hi/kn/ta/te.
- Eligibility reasoning template with standardized outputs.
- Chat history + session persistence.

### Phase 4: Hardening and observability (Week 8)
- Redis caching + background workers.
- Metrics, logs, tracing.
- Security testing and API rate limiting.

### Phase 5: Beta release (Week 9)
- UAT with real scheme documents.
- Performance tuning and prompt refinements.
- Production deployment + runbooks.

---

## 9) GitHub collaboration strategy

### Branching model
- `main`: production-ready only.
- `develop`: integration branch.
- Feature branches: `feature/<scope>-<short-desc>`.
- Hotfix branches: `hotfix/<issue-id>`.

### PR standards
- Mandatory PR template:
  - context/problem
  - approach
  - screenshots (for UI)
  - testing evidence
  - rollout / rollback notes
- Require at least **1 backend + 1 frontend** reviewer for cross-cutting PRs.
- Use CODEOWNERS for auto-review routing.

### CI checks
- Lint + type checks (frontend/backend).
- Unit tests + API contract tests.
- Security scan (pip/npm audit + SAST).
- Docker build validation.

### Release strategy
- Semantic version tags (`v0.1.0`, `v0.2.0`).
- Changelog generated from conventional commits.
- Staging deploy on merge to `develop`, production on approved release tags.

---

## 10) Task breakdown for 4 team members

### Member A — Backend & API Lead
- Build FastAPI skeleton, auth, and document/query routes.
- Create DB models, migrations, and API contracts.
- Implement caching, validation, and rate limits.

### Member B — AI/RAG Engineer
- Implement parsing/chunking/embedding pipeline.
- Integrate LangChain retriever + Sarvam prompts.
- Build eligibility decision templates and evaluation suite.

### Member C — Frontend Engineer
- Build Next.js app pages and reusable components.
- Implement upload, chat, citations, and language switch UI.
- Integrate APIs using Axios + React Query.

### Member D — DevOps & QA Engineer
- Create Docker Compose environment and Nginx config.
- Set up GitHub Actions CI/CD and environment secrets.
- Build test automation, load tests, and monitoring dashboards.

### Shared ceremonies
- Daily standup (15 min)
- Twice-weekly architecture sync
- Weekly demo + retro
- Definition of done includes docs + tests + observability hooks

---

## Suggested MVP acceptance criteria

- Upload and parse at least 3 real scheme PDFs successfully.
- Query response in under 5 seconds for cached docs.
- Answers include at least one valid citation for every response.
- Translation available in hi/kn/ta/te with readable quality.
- Eligibility answer uses standardized verdict categories.
