# GitHub Issues Backlog — AI Government Scheme Interpreter

Use the following issue drafts directly in GitHub Issues. Each issue includes title, description, checklist, expected outcome, and relevant folders.

---

## Issue 1: Build PDF upload interface

**Area:** Frontend development  
**Title:** Build PDF upload interface

**Description**
Create a user-friendly upload flow in the Next.js app for scheme PDFs. Include file picker, upload progress, success/error states, and display of generated document ID for downstream Q&A.

**Tasks checklist**
- [ ] Build upload page UI with drag-and-drop and file picker
- [ ] Validate file type (`.pdf`) and size limits
- [ ] Integrate `POST /api/v1/documents/upload` via Axios
- [ ] Add loading, success, and error states
- [ ] Persist returned `document_id` in state for chat usage
- [ ] Add basic component tests for upload behavior

**Expected outcome**
Users can upload a scheme PDF and receive a valid `document_id` with clear status feedback.

**Relevant folders**
- `frontend/src/app/upload/`
- `frontend/src/components/`
- `frontend/src/services/`
- `frontend/src/store/`

---

## Issue 2: Implement FastAPI document upload endpoint hardening

**Area:** Backend API development  
**Title:** Implement FastAPI document upload endpoint hardening

**Description**
Strengthen the document upload API for production readiness: input validation, robust error handling, async processing path, and structured responses.

**Tasks checklist**
- [ ] Add MIME/type and file size validation
- [ ] Improve exception handling and standardized error schema
- [ ] Move ingestion to background task/queue (non-blocking request)
- [ ] Add request/response logging with request IDs
- [ ] Add unit/integration tests for success and failure cases
- [ ] Update API docs with payload/response examples

**Expected outcome**
The upload endpoint is reliable under normal and failure scenarios and is ready for production-like traffic.

**Relevant folders**
- `backend/app/api/v1/`
- `backend/app/services/`
- `backend/app/schemas/`
- `backend/tests/` (to be added)

---

## Issue 3: Improve RAG retrieval pipeline

**Area:** RAG pipeline development  
**Title:** Improve RAG retrieval pipeline

**Description**
Improve retrieval quality by refining chunking, metadata filtering, and retrieval/reranking logic so eligibility answers are grounded and citation quality improves.

**Tasks checklist**
- [ ] Replace fixed chunking with heading-aware semantic chunking
- [ ] Add metadata filters (scheme/year/state/section)
- [ ] Add hybrid retrieval (semantic + keyword)
- [ ] Add reranking stage for top-k contexts
- [ ] Add hallucination guard when citations are weak
- [ ] Create evaluation script with baseline metrics (precision@k, citation validity)

**Expected outcome**
Higher answer relevance and better citation grounding across representative scheme questions.

**Relevant folders**
- `rag/`
- `vector_db/`
- `backend/app/services/rag_service.py`
- `backend/app/services/ingestion_service.py`
- `backend/app/services/vector_store_service.py`

---

## Issue 4: Add multilingual translation support validation

**Area:** RAG pipeline / Backend API development  
**Title:** Add multilingual translation support

**Description**
Complete and validate multilingual translation for Hindi, Kannada, Tamil, and Telugu, with fallback and quality checks.

**Tasks checklist**
- [ ] Confirm Sarvam translation API contract and payload format
- [ ] Add robust retries and timeout handling
- [ ] Preserve numerals, scheme names, and key legal terms
- [ ] Add language toggle support in frontend chat output
- [ ] Add tests for translation fallback behavior
- [ ] Document known translation limitations

**Expected outcome**
Answer responses are reliably available in `hi`, `kn`, `ta`, and `te` with readable quality and safe fallbacks.

**Relevant folders**
- `backend/app/services/sarvam_service.py`
- `backend/app/api/v1/routes_query.py`
- `frontend/src/app/chat/`
- `frontend/src/services/`
- `utils/language_map.py`

---

## Issue 5: Setup CI/CD pipeline

**Area:** DevOps and deployment  
**Title:** Setup CI/CD pipeline

**Description**
Implement CI/CD automation for linting, tests, build validation, and environment-based deployment gates.

**Tasks checklist**
- [ ] Add GitHub Actions workflow for backend lint/tests
- [ ] Add GitHub Actions workflow for frontend lint/build
- [ ] Add dependency vulnerability checks
- [ ] Add Docker build validation for backend/frontend
- [ ] Add branch protection rules for `develop` and `main`
- [ ] Add release workflow for `develop` → `main` promotion

**Expected outcome**
Automated quality gates prevent regressions and streamline safe releases.

**Relevant folders**
- `.github/workflows/` (to be added)
- `backend/`
- `frontend/`
- `scripts/`
- `docs/`

