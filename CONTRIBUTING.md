# Contributing to AI Government Scheme Interpreter

Thanks for contributing! This guide defines how our 4-member team collaborates effectively across frontend, backend, RAG, and DevOps.

## Workflow overview

- `main` → stable production code
- `develop` → active development and integration
- `feature/*` → individual feature branches

All day-to-day work happens in `feature/*` branches and merges into `develop` through Pull Requests.
Only release-ready code is promoted from `develop` to `main`.

## 1) Branch naming conventions

Use lowercase, hyphen-separated branch names:

```text
feature/<scope>-<short-description>
```

Recommended scopes:

- `frontend`
- `backend`
- `rag`
- `devops`
- `docs`
- `qa`

Examples:

- `feature/frontend-ui`
- `feature/backend-api`
- `feature/rag-pipeline`
- `feature/devops-setup`

## 2) Development workflow

1. Sync local branches:
   ```bash
   git checkout develop
   git pull origin develop
   ```
2. Create a feature branch.
3. Implement code + tests + documentation.
4. Run local quality checks before pushing.
5. Open PR to `develop`.
6. Address review comments and merge after approvals.
7. Periodically release `develop` into `main` when production-ready.

## 3) How to create feature branches

Always branch from `develop`:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/<scope>-<short-description>
```

Push your branch:

```bash
git push -u origin feature/<scope>-<short-description>
```

## 4) Pull request workflow

- **Base branch:** `develop` (for regular feature work)
- **Compare branch:** your `feature/*` branch

PR description must include:

- Summary of changes
- Why the change is needed
- Testing evidence (commands + results)
- Screenshots for UI changes
- Rollback considerations (if applicable)

Merge policy:

- CI must pass
- Required reviewers must approve
- Prefer **Squash and merge** into `develop`
- Delete feature branch after merge

## 5) How to submit pull requests

1. Ensure commits are clean and tests pass.
2. Rebase or merge latest `develop` to resolve conflicts.
3. Push branch updates.
4. Open PR to `develop`.
5. Request reviewers (at least one owner from impacted area).
6. Respond to comments quickly and push fixes.

## 6) Commit message format

Use Conventional Commit style:

```text
<type>(<scope>): <short summary>
```

Common types:

- `feat` → new functionality
- `fix` → bug fix
- `docs` → documentation changes
- `refactor` → code restructuring without behavior change
- `test` → tests added/updated
- `chore` → maintenance tasks

Examples:

- `feat(backend): add document upload endpoint`
- `feat(rag): add chunk reranking logic`
- `fix(frontend): handle upload error state`
- `docs(repo): add contributing guide`

## 7) Code review process

### Reviewer expectations

- Validate correctness and edge cases
- Verify tests and local reproducibility
- Check security/privacy implications (PDF handling, auth, PII)
- Confirm architecture alignment with `docs/system-architecture-and-development-plan.md`

### Approval policy (team of 4)

- Minimum 1 approval from area owner
- Cross-functional changes should have 2 approvals when possible
- No self-merge without at least 1 review approval (except emergency hotfixes)

### Review SLA

- First review target: within 1 business day
- Author should respond to comments within 1 business day

## Team ownership suggestion

- Frontend engineer: `frontend/`
- Backend engineer: `backend/`, `database/`
- AI/RAG engineer: `rag/`, `vector_db/`, AI services in `backend/app/services/`
- DevOps/QA engineer: `scripts/`, CI/CD workflows, deployment config

---

For branch strategy details, see also: `docs/git-workflow.md`.
