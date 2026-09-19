# Project Memory — AI Evidence Canvas

## System & Environment Notes
- **OS**: Windows (cp1252 encoding).
- **Backend Startup**:
  - `PYTHONIOENCODING="utf-8"` or avoid non-ASCII symbols (e.g. `✓`) in print statements to prevent startup `UnicodeEncodeError`.
  - Backend command: `cd backend && python -m uvicorn app.main:app --reload --port 8000`.

## API Contracts & Specifications
- **Workspaces**:
  - `GET /api/workspaces` -> returns `{ "workspaces": [...] }` (array must be unwrapped on frontend).
  - `POST /api/workspaces` -> requires `name` (min_length=1, trimmed, non-blank).
  - `PATCH /api/workspaces/{id}` -> update fields (do not use `PUT`).
  - Fields returned: `id`, `name`, `description`, `created_at`, `updated_at`, `evidence_count`, `relationship_count`.
- **Search & AI**:
  - `POST /api/workspaces/{id}/search` -> payload `{ "query": "...", "workspace_id": "..." }`.
  - `POST /api/workspaces/{id}/ask` -> payload `{ "question": "...", "workspace_id": "..." }`.

## Automated Testing Setup
- Browser & E2E tests are located in `scratch/browser_test.py` using Playwright async.
- Runs 43 assertions covering Landing Page, Workspace Manager, Modal Flows, Canvas Views, AI Assistant, and JS console checks.
