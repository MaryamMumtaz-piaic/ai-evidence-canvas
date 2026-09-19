# CLAUDE.md — AI Evidence Canvas

This file provides context for AI assistants (Claude, Gemini, etc.) working on this codebase.

## Project Purpose
AI Evidence Canvas is a visual investigation workspace. Users collect evidence (PDFs, URLs, notes, emails, images), AI analyzes it, extracts entities and relationships, and displays everything on an infinite visual canvas.

## Architecture Summary
- **Frontend**: Pure HTML/CSS/JS (Tailwind + Lucide Icons). No framework.
- **Backend**: FastAPI (Python 3.11+). Async throughout.
- **AI**: OpenAI GPT-4.1-mini for analysis. text-embedding-3-small for RAG.
- **Storage**: JSON files in `backend/data/`. No database.

## Key Files

### Backend Entry Point
`backend/app/main.py` — FastAPI app with all routers

### Core Services
- `backend/app/services/ingestion.py` — Main processing pipeline
- `backend/app/services/ai.py` — OpenAI wrapper
- `backend/app/services/embeddings.py` — Embedding + chunking
- `backend/app/services/retrieval.py` — RAG search
- `backend/app/services/relationship_engine.py` — Relationship detection

### Frontend Entry Points
- `frontend/index.html` — Landing page
- `frontend/workspace.html` — Workspace dashboard  
- `frontend/canvas.html` — Investigation canvas (main app)

### Key Frontend JS
- `frontend/assets/js/workspace-manager.js` — Main orchestrator
- `frontend/assets/js/canvas.js` — Infinite canvas engine
- `frontend/assets/js/evidence-cards.js` — Card management
- `frontend/assets/js/relationship-lines.js` — SVG connections

## Data Models

### Evidence
```json
{
  "id": "ev_xxx",
  "workspace_id": "ws_xxx",
  "type": "pdf|image|url|note|email|text",
  "title": "",
  "content": "",
  "summary": "",
  "entities": [{"name": "", "type": ""}],
  "topics": [],
  "status": "uploading|processing|analyzing|finding_relationships|ready|failed",
  "canvas_position": {"x": 0, "y": 0, "width": 280, "height": 200}
}
```

### Relationship
```json
{
  "source_evidence_id": "ev_001",
  "target_evidence_id": "ev_002",
  "relationship": "mentions|supports|contradicts|same_person|...",
  "confidence": 0.91,
  "reason": ""
}
```

## Common Tasks

### Add a new evidence type
1. Add to `EvidenceType` enum in `backend/app/models/evidence.py`
2. Add extraction logic in `backend/app/services/extraction.py`
3. Add API route in `backend/app/api/evidence.py`
4. Add frontend handling in `frontend/assets/js/evidence-cards.js`

### Add a new relationship type
1. Add to `RelationshipType` enum in `backend/app/models/relationship.py`
2. Update prompt in `backend/app/services/ai.py` `detect_relationships()`
3. Add color/style in `frontend/assets/js/relationship-lines.js`

### Modify the RAG pipeline
See `backend/app/services/retrieval.py` for retrieval and `backend/app/services/ai.py` for the answer generation.

## Environment Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Add OPENAI_API_KEY to .env
python seed_demo.py
uvicorn app.main:app --reload
```

## Testing
```bash
cd backend && pytest tests/ -v
```

## Important Constraints
- Never add database dependencies (no PostgreSQL, Redis, MongoDB)
- Never expose OPENAI_API_KEY to frontend JavaScript
- All AI JSON must be validated with Pydantic before use
- Canvas positions are saved via PATCH /api/evidence/{id}
- Background processing uses FastAPI BackgroundTasks
