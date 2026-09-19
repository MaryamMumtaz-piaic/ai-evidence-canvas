# AI Evidence Canvas

> A visual intelligence workspace where evidence becomes connected knowledge.

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4.1--mini-412991?logo=openai&logoColor=white)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

**AI Evidence Canvas** is a professional investigation and research workspace. Users collect evidence — PDFs, URLs, notes, emails, and images — and the AI automatically analyzes each item, extracts entities and events, detects relationships between evidence, and displays everything on an infinite interactive canvas.

The primary experience is the **visual canvas**, not a chatbot. Evidence becomes a connected knowledge graph that investigators can explore, filter, and query.

Built for: legal research, product investigations, security incidents, business intelligence, and evidence-based analysis.

---

## ✨ Features

- 🗺️ **Infinite Visual Canvas** — Drag, zoom, and pan across connected evidence cards
- 🤖 **AI Relationship Detection** — Automatically discovers connections between evidence items
- 💬 **RAG-Powered Q&A** — Ask questions, get answers grounded in your evidence with source citations
- 📄 **Multi-Format Evidence** — PDF, Images, URLs, Notes, Emails, Text files
- 🔍 **Entity Extraction** — People, organizations, contracts, events, dates extracted automatically
- 📅 **Timeline View** — Chronological evidence exploration
- 🕸️ **Graph View** — Visual relationship network with force-directed layout
- 🔎 **Semantic Search** — RAG-powered search across all evidence
- 📊 **Evidence Quality Scoring** — Know what's been analyzed at a glance
- 💾 **Persistent Workspaces** — Canvas positions and state survive page refresh
- 📤 **Export** — Investigation summaries as JSON
- 🎭 **Demo Workspace** — Pre-loaded "Product Pricing Investigation" with 10 evidence items and 14 relationships

---

## 🏗️ Architecture

```
Browser (Frontend)
     │
     ▼
FastAPI Backend (port 8000)        ← Serves BOTH frontend + API
     │
     ├── /api/*          → API routes (workspaces, evidence, search, RAG)
     ├── /               → Frontend static files (index.html, canvas.html, etc.)
     └── /docs           → Auto-generated API documentation
          │
          ▼
     OpenAI API
     (GPT-4.1-mini + text-embedding-3-small)
          │
          ▼
     Local JSON Storage
     (backend/data/)
```

```
ai-evidence-canvas/
│
├── frontend/                   — HTML5 + Tailwind CSS + Vanilla JS
│   ├── index.html              — Landing page
│   ├── workspace.html          — Workspace dashboard
│   ├── canvas.html             — Investigation canvas (main app)
│   ├── assets/
│   │   ├── css/main.css        — Design system & animations
│   │   └── js/
│   │       ├── api.js          — Centralized API client
│   │       ├── utils.js        — Shared utilities & toasts
│   │       ├── canvas.js       — Infinite canvas engine
│   │       ├── evidence-cards.js   — Draggable card management
│   │       ├── relationship-lines.js — SVG connection renderer
│   │       ├── ai-panel.js     — AI chat panel
│   │       ├── timeline.js     — Timeline view
│   │       ├── graph-view.js   — Graph visualization
│   │       ├── filters.js      — Filter system
│   │       ├── source-viewer.js — Evidence source viewer
│   │       └── workspace-manager.js — Main orchestrator
│   └── components/
│
├── backend/                    — Python FastAPI
│   ├── app/
│   │   ├── main.py             — FastAPI app entry point
│   │   ├── config.py           — Settings (pydantic-settings)
│   │   ├── api/                — Route handlers
│   │   │   ├── workspaces.py
│   │   │   ├── evidence.py
│   │   │   ├── search.py
│   │   │   ├── relationships.py
│   │   │   └── export.py
│   │   ├── models/             — Data models
│   │   │   ├── workspace.py
│   │   │   ├── evidence.py
│   │   │   ├── relationship.py
│   │   │   └── entity.py
│   │   ├── schemas/            — Pydantic API schemas
│   │   ├── services/           — Business logic
│   │   │   ├── ai.py           — OpenAI wrapper
│   │   │   ├── ingestion.py    — Processing pipeline
│   │   │   ├── extraction.py   — Text extraction (PDF, URL, image)
│   │   │   ├── embeddings.py   — Chunking + embedding generation
│   │   │   ├── retrieval.py    — RAG search
│   │   │   ├── relationship_engine.py — Relationship detection
│   │   │   └── timeline.py     — Timeline builder
│   │   └── storage/            — JSON persistence layer
│   │       ├── workspace_store.py
│   │       ├── evidence_store.py
│   │       └── vector_store.py
│   ├── data/                   — Local data storage (gitignored)
│   │   ├── workspaces/
│   │   ├── evidence/
│   │   ├── embeddings/
│   │   ├── relationships/
│   │   ├── exports/
│   │   ├── uploads/
│   │   └── demo/               — Pre-loaded demo data (committed)
│   ├── tests/                  — Pytest test suite
│   ├── seed_demo.py            — Demo data seeder
│   └── requirements.txt
│
├── .env.example                — Environment variable template
├── .gitignore
├── README.md
├── CLAUDE.md                   — AI assistant context
├── AGENT.md                    — AI agent contribution guide
├── CONTRIBUTING.md
└── LICENSE
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, Tailwind CSS (CDN), Vanilla JavaScript (ES6) |
| Icons | Lucide Icons |
| Backend | Python 3.11+, FastAPI, Uvicorn |
| Validation | Pydantic v2 |
| AI | OpenAI GPT-4.1-mini (analysis), text-embedding-3-small (RAG) |
| PDF Extraction | PyPDF |
| URL Extraction | httpx + BeautifulSoup4 |
| Storage | JSON files (zero-dependency MVP) |

---

## 🔄 RAG Pipeline

```
Upload Evidence (PDF / URL / Note / Image / Email)
      ↓
Text Extraction
  PDF     → PyPDF page extraction
  URL     → httpx fetch + BeautifulSoup content parsing
  Image   → GPT-4.1-mini vision analysis
  Note    → Direct text
  Email   → Header + body parsing
      ↓
Cleaning & Chunking (1000 chars, 200 overlap, sentence boundaries)
      ↓
Embedding Generation (text-embedding-3-small via OpenAI API)
      ↓
Vector Storage (cosine similarity index in local JSON)
      ↓
── User asks a question ──
      ↓
Query Embedding
      ↓
Cosine Similarity Search (top-k chunks)
      ↓
Context Assembly
      ↓
GPT-4.1-mini generates grounded answer with source citations
```

---

## 🧠 AI Relationship Pipeline

```
Evidence Added
      ↓
Entity & Topic Extraction (GPT-4.1-mini structured output)
  → People, Organizations, Contracts, Events, Dates, Locations
      ↓
Compare with All Existing Evidence in Workspace
      ↓
Relationship Detection (GPT-4.1-mini)
  Types: mentions, refers_to, same_person, same_organization,
         same_event, same_date, supports, contradicts, before, after, related_to
      ↓
Confidence Scoring (threshold: 0.7)
      ↓
Visual Connection drawn on Canvas with animated SVG line
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/MaryamMumtaz-piaic/ai-evidence-canvas.git
cd ai-evidence-canvas

# 2. Set up Python environment
cd backend
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
# source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env      # Windows
# cp .env.example .env      # Mac/Linux

# Open .env and add your key:
# OPENAI_API_KEY=sk-...

# 5. Seed demo data
python seed_demo.py
```

### ▶️ Run the App (Single Command)

```bash
# From the backend/ directory:
uvicorn app.main:app --reload --port 8000
```

That's it. One command runs everything — backend API **and** frontend.

| URL | Description |
|-----|-------------|
| `http://localhost:8000` | App (landing page) |
| `http://localhost:8000/docs` | Interactive API docs |
| `http://localhost:8000/health` | Health check |

---

## 📡 API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/workspaces` | Create workspace |
| `GET` | `/api/workspaces` | List all workspaces |
| `GET` | `/api/workspaces/{id}` | Get workspace |
| `PATCH` | `/api/workspaces/{id}` | Update workspace |
| `DELETE` | `/api/workspaces/{id}` | Delete workspace |
| `GET` | `/api/workspaces/{id}/evidence` | List evidence |
| `POST` | `/api/evidence/note` | Add note evidence |
| `POST` | `/api/evidence/url` | Add URL evidence |
| `POST` | `/api/evidence/upload` | Upload file (PDF/image/text) |
| `GET` | `/api/evidence/{id}` | Get evidence item |
| `PATCH` | `/api/evidence/{id}` | Update (canvas position, etc.) |
| `DELETE` | `/api/evidence/{id}` | Delete evidence |
| `POST` | `/api/workspaces/{id}/ask` | RAG Q&A |
| `POST` | `/api/workspaces/{id}/search` | Semantic search |
| `POST` | `/api/workspaces/{id}/analyze` | Trigger AI relationship analysis |
| `GET` | `/api/workspaces/{id}/relationships` | Get all relationships |
| `GET` | `/api/workspaces/{id}/timeline` | Timeline events |
| `GET` | `/api/workspaces/{id}/graph` | Graph nodes + edges |
| `POST` | `/api/workspaces/{id}/export` | Export investigation report |

Full interactive docs available at `/docs` (Swagger UI).

---

## 🎭 Demo Workflow

1. Run the app and open `http://localhost:8000`
2. Click **"Start Investigation"** → workspace dashboard
3. Open the pre-loaded **"Product Pricing Investigation"** workspace
4. Explore 10 connected evidence cards on the infinite canvas
5. Click any card to see extracted entities, topics, and connections
6. Click a connection line to see **why** AI linked those two pieces of evidence
7. Try asking: *"What evidence connects the price increase to the contract violation?"*
8. Switch to **Timeline** view to see events in chronological order
9. Add new evidence: drag-drop a PDF or paste a URL

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v
```

---

## 🔐 Security

- `OPENAI_API_KEY` stored in `.env` only — never exposed to frontend
- File uploads validated for type, extension, and size (max 50MB)
- Extracted HTML sanitized with BeautifulSoup
- URL fetching restricted to HTTP/HTTPS only
- All AI-generated JSON validated with Pydantic before use
- Malformed documents handled gracefully with error states

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

MIT — see [LICENSE](LICENSE)

---

Built by [Maryam Mumtaz](https://maryam-mumtaz.vercel.app) · [LinkedIn](https://www.linkedin.com/in/maryam-mumtaz-/) · [GitHub](https://github.com/MaryamMumtaz-piaic)
