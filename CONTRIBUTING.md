# Contributing to AI Government Scheme Interpreter

This guide helps a **4-member team** collaborate effectively across frontend, backend, RAG, and DevOps.

## Team collaboration model (4 members)

- **Frontend engineer**: `frontend/`
- **Backend engineer**: `backend/`, `database/`
- **AI/RAG engineer**: `rag/`, `vector_db/`, `backend/app/services/`
- **DevOps/QA engineer**: `scripts/`, CI/CD, release process

## 1) Branch naming rules

Use this naming pattern:

```text
feature/<scope>-<short-description>
```

Examples:

- `feature/frontend-ui`
- `feature/backend-api`
- `feature/rag-pipeline`
- `feature/devops-setup`

Branch model:

- `main` → stable production code
- `develop` → active integration branch
- `feature/*` → individual developer branches

## 2) Pull request guidelines

- Open PRs from `feature/*` to `develop`.
- Include in every PR:
  - summary of change
  - motivation/business context
  - testing commands and outcomes
  - screenshots for UI changes
- Keep PRs small and focused for faster review.
- Use squash merge into `develop` after approval.

Release flow:

- `develop` → `main` only for verified release-ready code.

## 3) Commit message format

Use Conventional Commits:

```text
<type>(<scope>): <short summary>
```

Examples:

- `feat(frontend): add citation viewer component`
- `feat(backend): add auth login endpoint`
- `fix(rag): improve hybrid retrieval scoring`
- `docs(repo): update development workflow`

Recommended types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.

## 4) Development workflow

1. Sync `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   ```
2. Create a feature branch:
   ```bash
   git checkout -b feature/<scope>-<short-description>
   ```
3. Build + test locally.
4. Push branch and open PR into `develop`.
5. Address review comments.
6. Merge after approvals and passing checks.
7. Promote `develop` to `main` only through a release PR.

## 5) Code review process

Review goals:

- correctness and edge cases
- security/privacy implications
- test coverage and reproducibility
- architecture alignment with project docs

Approval policy:

- minimum 1 reviewer approval required
- cross-cutting changes should get 2 approvals when possible
- no direct pushes to `main`

Review SLA:

- first review target: within 1 business day
- author response target: within 1 business day
