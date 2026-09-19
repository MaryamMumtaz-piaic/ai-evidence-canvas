# AI Evidence Canvas

> A visual intelligence workspace where evidence becomes connected knowledge.

[Badge: Python 3.11+] [Badge: FastAPI] [Badge: OpenAI] [Badge: License MIT]

<!-- Hero image placeholder or ASCII art showing canvas -->

## Overview

AI Evidence Canvas is a professional investigation and research workspace...
[Full description of what the app does, key value prop]

## ✨ Features

- 🗺️ **Infinite Visual Canvas** — Drag, zoom, and pan across connected evidence
- 🤖 **AI Relationship Detection** — Automatically discovers connections between evidence
- 💬 **RAG-Powered Q&A** — Ask questions, get answers grounded in your evidence with citations
- 📄 **Multi-Format Evidence** — PDF, Images, URLs, Notes, Emails
- 🔍 **Entity Extraction** — People, organizations, events, dates extracted automatically  
- 📅 **Timeline View** — Chronological evidence exploration
- 🕸️ **Graph View** — Visual relationship network
- 🔎 **Smart Search** — Semantic search across all evidence
- 📊 **Evidence Quality Scoring** — Know what's been analyzed
- 💾 **Persistent Workspaces** — Canvas positions survive page refresh
- 📤 **Export** — Investigation summaries as JSON

## 🏗️ Architecture

[Mermaid or ASCII diagram showing: Frontend → FastAPI → OpenAI, with Storage layer]

```
frontend/           — HTML5 + Tailwind CSS + Vanilla JS
  ├── index.html    — Landing page
  ├── workspace.html — Workspace dashboard
  └── canvas.html   — Investigation canvas
  
backend/            — Python FastAPI
  ├── app/
  │   ├── api/      — Route handlers
  │   ├── services/ — AI/RAG/Processing logic
  │   ├── models/   — Data models
  │   ├── schemas/  — API validation
  │   └── storage/  — JSON persistence layer
  └── data/         — Local data storage
```

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, Tailwind CSS, Vanilla JavaScript |
| Backend | Python 3.11, FastAPI, Uvicorn |
| AI | OpenAI GPT-4.1-mini, text-embedding-3-small |
| Storage | JSON files (MVP) |
| Icons | Lucide |

## 🔄 RAG Pipeline

```
Upload Evidence
      ↓
Text Extraction (PyPDF / Vision AI / BeautifulSoup)
      ↓
Cleaning & Chunking (1000 tokens, 200 overlap)
      ↓
Embedding Generation (text-embedding-3-small)
      ↓
Vector Storage (local JSON)
      ↓
[User asks question]
      ↓
Query Embedding
      ↓
Cosine Similarity Search
      ↓
Context Assembly
      ↓
GPT-4.1-mini Answer with Source Citations
```

## 🧠 AI Relationship Pipeline

```
Evidence Added
      ↓
Entity & Topic Extraction
      ↓
Compare with Existing Evidence
      ↓
Relationship Detection (GPT-4.1-mini)
      ↓
Confidence Scoring (threshold: 0.7)
      ↓
Visual Connection on Canvas
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/MaryamMumtaz-piaic/ai-evidence-canvas.git
cd ai-evidence-canvas

# Set up backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Seed demo data
python seed_demo.py
```

### Running the Application

```bash
# Start backend (from backend/ directory)
uvicorn app.main:app --reload --port 8000

# Open frontend
# Simply open frontend/index.html in your browser
# Or use VS Code Live Server extension
# Or: python -m http.server 3000 (from frontend/ directory)
```

### Access
- Frontend: `http://localhost:3000` (or open index.html directly)
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## 📡 API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/workspaces | Create workspace |
| GET | /api/workspaces | List workspaces |
| GET | /api/workspaces/{id} | Get workspace |
| POST | /api/evidence/note | Add note evidence |
| POST | /api/evidence/url | Add URL evidence |
| POST | /api/evidence/upload | Upload file evidence |
| POST | /api/workspaces/{id}/ask | RAG Q&A |
| POST | /api/workspaces/{id}/search | Semantic search |
| GET | /api/workspaces/{id}/relationships | Get relationships |
| GET | /api/workspaces/{id}/timeline | Timeline events |
| GET | /api/workspaces/{id}/graph | Graph data |
| POST | /api/workspaces/{id}/analyze | Trigger AI analysis |

## 🎭 Demo Workflow

1. Open the app and go to the workspace dashboard
2. The demo workspace "Product Pricing Investigation" is pre-loaded
3. Click to open — you'll see 10 connected evidence cards
4. Click any card to see entities, topics, and connections
5. Click a connection line to see why AI linked these pieces
6. Try asking: "What evidence connects the price increase to the contract violation?"
7. Switch to Timeline view to see events chronologically
8. Add new evidence: drop a PDF or paste a URL

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v
```

## 📁 Project Structure

[Full directory tree]

## 🔐 Security

- API keys stored in environment variables only
- File uploads validated for type and size
- HTML content sanitized
- URL fetching restricted to HTTP/HTTPS
- No API keys exposed to frontend

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

MIT — see [LICENSE](LICENSE)

---

Built by [Maryam Mumtaz](https://maryam-mumtaz.vercel.app) | [LinkedIn](https://www.linkedin.com/in/maryam-mumtaz-/) | [GitHub](https://github.com/MaryamMumtaz-piaic)
