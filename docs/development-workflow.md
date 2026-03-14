# Development Workflow

This repository follows a three-branch collaboration model to keep production stable while enabling active team development.

## Branch strategy

- `main` → production/stable code
- `develop` → integration branch for active development
- `feature/*` → individual developer branches

## How the workflow works

1. **Start from `develop`**
   - Pull latest changes from `develop` before starting work.
2. **Create a feature branch**
   - Use a focused branch for each feature/fix.
3. **Open Pull Request into `develop`**
   - All regular development merges into `develop` only.
4. **Promote to `main`**
   - Only verified/reviewed release-ready code is merged from `develop` into `main`.

## Feature branch naming

Use the pattern:

```text
feature/<scope>-<short-description>
```

Examples:

- `feature/frontend-ui`
- `feature/backend-api`
- `feature/rag-pipeline`
- `feature/devops-setup`

## Typical git commands

```bash
# 1) Sync integration branch
git checkout develop
git pull origin develop

# 2) Create feature branch
git checkout -b feature/<scope>-<short-description>

# 3) Push and open PR to develop
git push -u origin feature/<scope>-<short-description>
```

## Merge rules

- Do **not** merge feature branches directly into `main`.
- Merge feature branches into `develop` via PR and review.
- Merge `develop` into `main` only for validated releases.
