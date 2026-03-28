# Commit history (for instructors / grading)

A clear Git history helps reviewers see **frontend**, **backend**, and **AI-related** work as separate steps.

## Suggested commit style

Use **imperative, short** messages (one line), optional body for context:

| Example message | Typical contents |
|-----------------|------------------|
| `feat(frontend): add resume upload and analyze form` | `frontend/` |
| `feat(backend): add FastAPI /api/analyze and hybrid score` | `backend/main.py` |
| `fix(backend): pin Python 3.11 for Render deploy` | `runtime.txt`, `requirements.txt` |
| `docs: expand README with AI methodology and usage` | `README.md`, `docs/` |
| `chore: add root gitignore for venv and node_modules` | `.gitignore` |

Prefixes like `feat:`, `fix:`, `docs:` are optional but make history easy to scan.

## What to commit

- **Do commit:** source code, `README.md`, `docs/`, `requirements.txt`, `package.json`, configs (`vercel.json`, `render.yaml`), Colab notebook.  
- **Do not commit:** `backend/venv/`, `frontend/node_modules/`, `.env` files with secrets (use `.env.example` only).

## If your history is already one big commit

You may still **add further commits** for documentation and fixes (`docs: …`, `fix: …`). Squashing is not required unless your course demands it.
