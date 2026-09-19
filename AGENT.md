# AGENT.md — AI Evidence Canvas

This document guides AI agents (Gemini, Claude, GPT, Cursor) in contributing to AI Evidence Canvas.

## Project Type
Full-stack web application. Python FastAPI backend + HTML/JS/CSS frontend.

## Before Making Changes

1. **Read CLAUDE.md** for architecture context
2. **Check the relevant service** before modifying API routes
3. **Search first**: grep for the function/class before opening full files
4. **Test locally**: `pytest tests/ -v` before submitting

## Code Style

### Python
- Use async/await throughout
- Pydantic for all data validation
- Type hints on all functions
- Docstrings on all public functions
- Handle OpenAI errors gracefully (fallback to empty results)

### JavaScript
- ES6 classes
- No frameworks (no React, Vue, Angular)
- Error handling on all API calls
- Toast notifications for user feedback
- Debounce API writes (especially canvas position saves)

## Key Patterns

### Background Evidence Processing
```python
# In API route:
background_tasks.add_task(ingestion.process_evidence, evidence_id, workspace_id)
return JSONResponse(status_code=202, content={"id": evidence_id, "status": "processing"})
```

### Adding a new API endpoint
1. Define Pydantic schema in `schemas/`
2. Add route in `api/`
3. Implement logic in `services/`
4. Write test in `tests/`

### Frontend API calls
```javascript
// Always use the api.js client
const result = await api.workspaces.get(workspaceId);
if (result.error) { showToast(result.error, 'error'); return; }
```

## What NOT to change
- Do not add databases (PostgreSQL, SQLite, Redis)
- Do not add authentication/user system (out of scope)
- Do not add Docker/K8s configs
- Do not modify demo data without running seed_demo.py
- Do not hardcode API keys anywhere

## Running the App
```bash
# Backend
cd backend && uvicorn app.main:app --reload

# Frontend (serve static files)
python -m http.server 3000 --directory frontend
```

## Data Flow
```
User uploads evidence
  → POST /api/evidence/upload
  → API creates Evidence record (status: uploading)
  → BackgroundTask: process_evidence()
    → Extract text
    → Generate summary + entities
    → Create embeddings
    → Detect relationships
    → Update status: ready
  → Frontend polls GET /api/evidence/{id} every 5s
  → Card updates on canvas when ready
```
