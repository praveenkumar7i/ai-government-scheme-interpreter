# Git Workflow Guide

This project follows a **three-tier branching model** to keep releases stable while enabling parallel development.

## Branching strategy

- `main` → production-ready code only
- `develop` → active integration branch for ongoing development
- `feature/*` → short-lived feature branches created by team members

## 1) How to create feature branches

Always branch from `develop` for new work:

```bash
git checkout develop
git pull origin develop
git checkout -b feature/<scope>-<short-description>
```

Examples:

- `feature/frontend-ui`
- `feature/backend-api`
- `feature/rag-pipeline`
- `feature/devops-setup`

## 2) How to open pull requests

When your feature is ready:

1. Commit small, logical changes with clear messages.
2. Push your branch:

```bash
git push -u origin feature/<scope>-<short-description>
```

3. Open a Pull Request with:
   - **Base branch:** `develop`
   - **Compare branch:** your `feature/*` branch
4. Include in PR description:
   - What changed
   - Why it changed
   - Test evidence (commands + outputs)
   - Screenshots for UI changes

## 3) How to merge into `develop`

PRs should be merged into `develop` after:

- CI checks pass (lint, tests, build)
- Required reviewers approve
- Merge conflicts are resolved

Recommended merge method:

- **Squash and merge** for clean history in `develop`.

After merge, delete the feature branch:

```bash
git branch -d feature/<scope>-<short-description>
git push origin --delete feature/<scope>-<short-description>
```

## 4) When code should go into `main`

`main` should only receive changes that are **production-ready**.

Promote code from `develop` to `main` when:

- Planned release scope is complete
- Regression and integration testing pass
- Release notes/changelog are prepared
- Team signs off for deployment

Suggested flow:

- Open PR from `develop` → `main`
- Tag release after merge (e.g., `v0.1.0`)


## Enforcement policy

- All future development must happen in `feature/*` branches and be merged via Pull Requests into `develop`.
- Direct commits to `main` are not allowed.
- Only verified and approved code is promoted from `develop` to `main` through a release PR.

## 5) Branch naming conventions

Use lowercase, hyphen-separated names.

Pattern:

```text
feature/<scope>-<short-description>
```

Common scopes:

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

---

## Quick reference

1. Create branch from `develop`
2. Build + test locally
3. Open PR to `develop`
4. Merge after approvals + green CI
5. Release from `develop` to `main` only when production-ready
