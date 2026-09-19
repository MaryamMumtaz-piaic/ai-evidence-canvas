# AI Evidence Canvas

## 1. Project Overview

Build a professional, UI-first **AI Evidence Canvas** — an interactive research and investigation workspace where users can collect documents, screenshots, URLs, notes, emails, and other evidence on an infinite visual canvas.

The system uses **RAG (Retrieval-Augmented Generation)** and AI analysis to understand evidence, extract entities and events, identify relationships, and automatically create connections between related evidence.

The primary product experience must be the **visual evidence canvas**, not a traditional dashboard or chatbot.

The final application should feel like a modern professional investigation/research product suitable for:

* Legal research
* Product investigations
* Security investigations
* Business research
* Internal investigations
* Research projects
* Evidence-based analysis

The application must be fully functional from frontend to backend.

---

# 2. Primary Product Goal

The user should be able to:

1. Create a research workspace.
2. Add different types of evidence.
3. See evidence as visual cards on an infinite canvas.
4. Have AI analyze each evidence item.
5. Extract entities, dates, topics, events, and claims.
6. Automatically discover relationships between evidence.
7. Display AI-generated connections visually.
8. Click any relationship to understand why the connection exists.
9. Open the original evidence/source.
10. Search the entire evidence collection using RAG.
11. Ask questions about the collected evidence.
12. Receive answers grounded in the available evidence.
13. Filter the canvas by evidence type, entity, topic, date, or confidence.
14. Explore evidence through a timeline.
15. Switch between canvas, timeline, and relationship views.

---

# 3. Core Experience

The main screen should look like a professional visual investigation workspace.

### Layout

```text
┌──────────────────────────────────────────────────────────────────┐
│ Logo │ Workspace │ Search │ Ask AI │ Filter │ Export │ Profile   │
├───────────────┬──────────────────────────────────────────────────┤
│               │                                                  │
│ Evidence      │                                                  │
│ Library       │              INFINITE CANVAS                     │
│               │                                                  │
│ + Add Evidence│       ┌────────────┐                             │
│               │       │ Evidence A │───────┐                     │
│ Documents     │       └────────────┘       │                     │
│ Screenshots   │                            ▼                     │
│ URLs          │                    ┌────────────┐                │
│ Notes         │                    │ Evidence B │                │
│ Emails        │                    └────────────┘                │
│               │                            │                     │
│               │                            ▼                     │
│               │                    ┌────────────┐                │
│               │                    │ Evidence C │                │
│               │                    └────────────┘                │
│               │                                                  │
├───────────────┴──────────────────────────────────────────────────┤
│ Zoom − 100% + │ Fit Canvas │ Timeline │ Graph │ Minimap          │
└──────────────────────────────────────────────────────────────────┘
```

The canvas must visually dominate the application.

---

# 4. Technology Stack

## Frontend

Use:

* HTML5
* Tailwind CSS
* Vanilla JavaScript
* SVG / Canvas APIs where appropriate
* Lucide Icons
* Drag-and-drop interactions
* Smooth transitions and micro-interactions

Do NOT build the interface as a generic admin dashboard.

The UI should feel like a modern research/investigation application.

## Backend

Use:

* Python 3.11+
* FastAPI
* Uvicorn
* Pydantic
* Python async/await

## AI

Use:

* OpenAI API
* GPT-4.1-mini or current equivalent available in the environment
* `text-embedding-3-small` for embeddings

AI must be used for:

* Evidence summarization
* Entity extraction
* Topic extraction
* Claim extraction
* Event extraction
* Relationship detection
* Evidence classification
* RAG question answering

## Storage

For the MVP use lightweight local persistence.

Suggested structure:

```text
data/
├── workspaces/
├── evidence/
├── embeddings/
├── relationships/
├── timelines/
└── exports/
```

JSON-based persistence is acceptable for the MVP.

Do not introduce unnecessary infrastructure such as PostgreSQL, Redis, Docker, or Kubernetes unless required.

---

# 5. Application Structure

Create the following major frontend views:

## 5.1 Landing Page

Create a polished marketing-style landing page.

Sections:

* Hero
* Product visualization
* How it works
* Evidence types
* AI relationship discovery
* RAG-powered investigation
* Use cases
* CTA

The hero should visually demonstrate connected evidence cards rather than using a generic illustration.

---

# 5.2 Workspace Dashboard

Show:

* Recent workspaces
* Evidence count
* Relationship count
* Recent activity
* Last investigation
* Quick create workspace

Example:

```text
My Investigations

┌──────────────────────────────┐
│ Product Pricing Investigation│
│ 28 Evidence · 16 Connections │
│ Updated 12 min ago           │
└──────────────────────────────┘

┌──────────────────────────────┐
│ Security Incident             │
│ 42 Evidence · 31 Connections │
└──────────────────────────────┘
```

---

# 5.3 Investigation Workspace

This is the primary screen.

Include:

### Top Navigation

* Workspace name
* Global search
* Ask AI
* Filters
* View switcher
* Export
* Settings

### Left Evidence Panel

Sections:

* All Evidence
* Documents
* Screenshots
* URLs
* Notes
* Emails

Each item should display:

* Icon
* Title
* Type
* Date
* Processing status

### Main Canvas

The infinite canvas must support:

* Pan
* Zoom
* Drag evidence cards
* Select cards
* Multi-select
* Connect cards
* Delete
* Duplicate
* Auto-layout
* Fit-to-screen
* Minimap

---

# 6. Evidence Types

Support at minimum:

### PDF

User uploads PDF documents.

Extract:

* Text
* Metadata
* Page references

### Text / Markdown

Support:

* `.txt`
* `.md`

### Screenshots / Images

Support:

* `.png`
* `.jpg`
* `.jpeg`
* `.webp`

For the MVP, analyze image content through an available vision-capable AI model.

### Website URL

User enters a URL.

Backend should:

1. Validate URL.
2. Fetch the page.
3. Extract readable content.
4. Remove unnecessary HTML.
5. Store source URL.
6. Chunk extracted content.
7. Generate embeddings.

### Notes

Users can create manual evidence.

### Email

Allow users to paste email content or upload an email text file.

Store:

* Sender
* Recipient
* Subject
* Date
* Body

---

# 7. Evidence Card

Every evidence item should become a visual card.

Example:

```text
┌───────────────────────────────┐
│ PDF                           │
│ contract-v2.pdf               │
│                               │
│ "Agreement between Company A  │
│ and Company B regarding..."   │
│                               │
│ Entities                      │
│ Company A · Company B         │
│                               │
│ Topics                        │
│ Contract · Payment · Renewal  │
│                               │
│ 4 connections                 │
│                               │
│ [Open] [Details]              │
└───────────────────────────────┘
```

Cards should have subtle visual differences based on evidence type.

Do not use excessive colors.

Keep the visual language professional.

---

# 8. Evidence Processing Pipeline

When evidence is added:

```text
Upload / URL / Note
        ↓
Validation
        ↓
Content Extraction
        ↓
Text Normalization
        ↓
Chunking
        ↓
Embedding Generation
        ↓
Metadata Extraction
        ↓
Entity Extraction
        ↓
Topic Extraction
        ↓
Claim Extraction
        ↓
Event Extraction
        ↓
Relationship Detection
        ↓
Canvas Update
```

Processing should happen asynchronously where appropriate.

Show processing states:

* Uploading
* Processing
* Analyzing
* Finding relationships
* Ready
* Failed

---

# 9. RAG Architecture

Implement a simple but real RAG pipeline.

## Ingestion

For every evidence item:

```text
Raw Evidence
      ↓
Text Extraction
      ↓
Cleaning
      ↓
Chunking
      ↓
Embedding
      ↓
Vector Storage
```

Each chunk must preserve metadata:

```json
{
  "evidence_id": "...",
  "chunk_id": "...",
  "source_type": "pdf",
  "source_name": "contract.pdf",
  "page": 4,
  "text": "...",
  "created_at": "..."
}
```

## Retrieval

When the user asks a question:

```text
User Question
      ↓
Query Embedding
      ↓
Similarity Search
      ↓
Top Relevant Chunks
      ↓
Context Assembly
      ↓
LLM
      ↓
Grounded Answer
```

---

# 10. Evidence-Grounded AI Chat

Create an **Ask AI** panel.

The user can ask questions such as:

* "What evidence connects Company A to the payment issue?"
* "Which documents mention the renewal date?"
* "Show me all evidence related to pricing."
* "What happened before the security incident?"
* "Which sources contradict each other?"

AI answers must be grounded in retrieved evidence.

Every important answer must include source references.

Example:

```text
The payment deadline appears to have changed from
June 15 to June 30.

Sources:
• contract-v2.pdf — Page 4
• email-june-12.txt
```

Clicking a source should open the corresponding evidence.

---

# 11. Entity Extraction

AI should identify entities such as:

* People
* Organizations
* Products
* Locations
* Dates
* IP addresses
* URLs
* Contracts
* Events
* Topics

Store extracted entities separately.

Example:

```json
{
  "name": "Company A",
  "type": "organization",
  "evidence_ids": ["ev_001", "ev_007"]
}
```

---

# 12. Relationship Detection

This is one of the most important features.

AI should inspect evidence metadata and retrieved content to detect relationships.

Possible relationship types:

* Mentions
* Refers to
* Same person
* Same organization
* Same event
* Same date
* Same topic
* Supports
* Contradicts
* Before
* After
* Related to

Example:

```json
{
  "source_evidence_id": "ev_001",
  "target_evidence_id": "ev_008",
  "relationship": "mentions",
  "confidence": 0.91,
  "reason": "Both documents reference the same contract number."
}
```

---

# 13. Visual Connections

Relationships must appear directly on the canvas.

Example:

```text
┌────────────┐
│ Contract   │
└─────┬──────┘
      │
      │ mentions
      │
      ▼
┌────────────┐
│ Email      │
└────────────┘
```

Connection lines should:

* Be animated subtly
* Display relationship labels on selection
* Support click interaction
* Show confidence
* Open relationship details

Do not create noisy lines between every card.

Only display meaningful relationships.

---

# 14. Relationship Inspector

When the user clicks a connection, open a right-side inspector.

Show:

```text
Relationship

Contract.pdf
       ↓
"mentions"
       ↓
Email #14

Confidence
91%

Why this connection exists

Both sources reference:
Contract #CT-2048

Supporting Evidence

Contract.pdf — Page 4
Email #14 — June 12
```

Include a button:

**View Supporting Evidence**

---

# 15. Source Viewer

Clicking an evidence card should open a source viewer.

For PDFs:

* Document preview
* Page navigation
* Search
* Highlight relevant text

For URLs:

* Source URL
* Extracted content
* Relevant passages

For notes/emails:

* Clean document viewer

For images:

* Image preview
* AI-generated analysis
* Extracted entities

---

# 16. Timeline View

Create a separate timeline mode.

Automatically detect dates from evidence.

Example:

```text
JAN 12
│
├── Contract Created
│
JAN 18
│
├── Pricing Email
│
FEB 02
│
├── Customer Complaint
│
FEB 05
│
└── Resolution
```

Users should be able to:

* Zoom timeline
* Filter by evidence
* Click events
* Jump to evidence on canvas

---

# 17. Relationship Graph View

Provide an alternative graph view.

Nodes:

* Evidence
* People
* Organizations
* Events
* Topics

Edges:

* Mentions
* Supports
* Contradicts
* Related
* Before
* After

Allow:

* Zoom
* Pan
* Node selection
* Filtering
* Focus on entity

The graph must remain readable even with many nodes.

---

# 18. Evidence Search

Implement global search.

Search should support:

* Evidence title
* Extracted text
* Entities
* Topics
* Dates
* Relationship types

Example:

```text
Search evidence...

"payment deadline"
```

Results:

```text
4 matching evidence items

contract-v2.pdf
email-june-12
invoice-2048
meeting-notes
```

---

# 19. Filters

Create a professional filter system.

Filters:

### Evidence Type

* PDF
* Image
* URL
* Note
* Email

### Entity

* Person
* Organization
* Product
* Event

### Relationship

* Supports
* Contradicts
* Mentions
* Related

### Date

* Before
* After
* Range

### Confidence

* High
* Medium
* Low

Filters should update the canvas dynamically.

---

# 20. AI Evidence Summary

When selecting multiple evidence items, allow:

**Summarize Selection**

AI should generate:

* Main findings
* Important entities
* Key dates
* Supporting evidence
* Contradictions
* Open questions

Every generated finding should link back to evidence.

---

# 21. AI Investigation Assistant

Create an optional assistant panel.

It should help users explore the investigation.

Example prompts:

```text
Find contradictions
Show evidence about pricing
Build a timeline
What evidence is missing?
Who appears most frequently?
Which sources support this claim?
```

The assistant should trigger actual retrieval and analysis instead of returning generic responses.

---

# 22. Evidence Quality

Each evidence item should have an analysis status.

Example:

```text
Evidence Quality

Text Extracted       ✓
Entities Found       ✓
Dates Found          ✓
Relationships        ✓
Embedding            ✓
```

If something fails, clearly display the error.

---

# 23. Workspace Persistence

Persist:

* Workspace
* Evidence
* Canvas positions
* Relationships
* Entities
* Timeline events
* Filters
* Notes

Canvas positions must survive page refresh.

Example:

```json
{
  "evidence_id": "ev_001",
  "x": 420,
  "y": 180,
  "width": 280,
  "height": 180
}
```

---

# 24. Workspace Actions

Support:

* Create workspace
* Rename workspace
* Delete workspace
* Add evidence
* Remove evidence
* Move evidence
* Connect evidence manually
* Delete relationship
* Auto-layout
* Search
* Filter
* Export

---

# 25. Export

Allow users to export:

### Investigation Summary

Generate a clean report containing:

* Investigation title
* Summary
* Evidence list
* Important entities
* Relationships
* Timeline
* AI findings
* Source references

### Canvas

Allow export as:

* PNG
* JSON

For the MVP, PNG and JSON are sufficient.

---

# 26. Validation

Validation must be handled properly on both frontend and backend.

## File Validation

Check:

* File exists
* Supported extension
* File size
* MIME type

## URL Validation

Check:

* Valid URL
* HTTP/HTTPS only
* Reject malformed URLs
* Handle unreachable websites

## Text Validation

Check:

* Empty content
* Excessively large input
* Invalid encoding

## AI Validation

Never trust raw AI JSON.

Validate all AI-generated structured data using Pydantic models.

---

# 27. Backend API

Create clean FastAPI routes.

Suggested endpoints:

```text
POST   /api/workspaces
GET    /api/workspaces
GET    /api/workspaces/{id}
DELETE /api/workspaces/{id}

POST   /api/workspaces/{id}/evidence
GET    /api/workspaces/{id}/evidence
GET    /api/evidence/{id}
DELETE /api/evidence/{id}

POST   /api/evidence/url
POST   /api/evidence/upload
POST   /api/evidence/note

POST   /api/workspaces/{id}/analyze
GET    /api/workspaces/{id}/relationships

POST   /api/workspaces/{id}/search
POST   /api/workspaces/{id}/ask

GET    /api/workspaces/{id}/timeline
GET    /api/workspaces/{id}/graph

POST   /api/workspaces/{id}/export
```

Keep API responsibilities clearly separated.

---

# 28. Suggested Backend Structure

```text
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── workspaces.py
│   │   ├── evidence.py
│   │   ├── search.py
│   │   ├── relationships.py
│   │   └── export.py
│   │
│   ├── models/
│   │   ├── workspace.py
│   │   ├── evidence.py
│   │   ├── relationship.py
│   │   └── entity.py
│   │
│   ├── services/
│   │   ├── ingestion.py
│   │   ├── extraction.py
│   │   ├── embeddings.py
│   │   ├── retrieval.py
│   │   ├── relationship_engine.py
│   │   ├── timeline.py
│   │   └── ai.py
│   │
│   ├── storage/
│   │   ├── workspace_store.py
│   │   ├── evidence_store.py
│   │   └── vector_store.py
│   │
│   └── schemas/
│       ├── workspace.py
│       ├── evidence.py
│       ├── relationship.py
│       └── ai.py
│
└── data/
```

---

# 29. Frontend Structure

```text
frontend/
│
├── index.html
├── workspace.html
├── evidence.html
├── settings.html
│
├── assets/
│   ├── css/
│   ├── js/
│   └── icons/
│
└── components/
```

Use reusable JavaScript components/modules for:

* Canvas
* Evidence cards
* Side panels
* Modals
* Search
* Filters
* Timeline
* Graph
* AI panel

---

# 30. Visual Design Requirements

The UI is extremely important.

The product should look like a **premium professional investigation/research application**.

### Design principles

* Clean
* Minimal
* Professional
* Information-dense but readable
* Strong visual hierarchy
* Excellent spacing
* Smooth animations
* Subtle shadows
* Rounded cards
* Clear typography
* Consistent iconography

Avoid:

* Generic Bootstrap appearance
* Excessive gradients
* Excessive glassmorphism
* Huge unnecessary hero sections inside the application
* Emoji-based UI
* Cluttered dashboards
* Random colors

---

# 31. Canvas Interaction Requirements

The canvas must feel polished.

Implement:

* Mouse-wheel zoom
* Click-drag pan
* Card dragging
* Selection
* Multi-selection
* Connection highlighting
* Auto-layout
* Fit-to-screen
* Minimap
* Zoom controls

When a card is selected:

* Highlight related cards
* Fade unrelated cards slightly
* Highlight connected edges
* Open evidence details

This interaction is a key visual selling point.

---

# 32. AI Relationship Animation

When AI discovers new relationships:

1. Evidence card receives subtle processing state.
2. Relationship line appears.
3. Connection animates into place.
4. Small AI-generated relationship label appears.
5. User can inspect the relationship.

Do not over-animate the interface.

---

# 33. Demo Data

Include realistic demo data so the application looks impressive immediately after launch.

Create one demo workspace:

**Product Pricing Investigation**

Include approximately:

* 8–12 evidence items
* PDFs
* Notes
* URLs
* Customer feedback
* Emails
* Screenshots

Create realistic relationships between them.

The demo should immediately show a meaningful evidence network.

---

# 34. Example Demo Investigation

Use a fictional company.

Example evidence:

```text
Customer Review
      ↓
Pricing Complaint
      ↓
Support Ticket
      ↓
Internal Pricing Note
      ↓
Product Meeting
      ↓
New Pricing Proposal
```

The canvas should visually communicate the investigation story.

---

# 35. Security Requirements

Implement basic security practices:

* Validate uploaded files
* Sanitize extracted HTML
* Never execute uploaded files
* Restrict URL fetching to HTTP/HTTPS
* Never expose API keys to frontend
* Store secrets in environment variables
* Validate all API input
* Limit upload sizes
* Handle malformed documents gracefully

---

# 36. Error Handling

The application must never silently fail.

Display clear states for:

* Upload failure
* Unsupported file
* URL fetch failure
* Extraction failure
* AI failure
* Embedding failure
* Retrieval failure
* Invalid workspace
* Missing evidence

Use professional inline error messages and toast notifications.

---

# 37. Loading States

Create polished loading states for:

* Evidence upload
* Document processing
* AI analysis
* Relationship discovery
* RAG retrieval
* Timeline generation
* Graph generation

Do not use a generic spinner everywhere.

Use contextual skeletons or processing indicators.

---

# 38. Testing

Implement tests for:

### Backend

* Workspace creation
* Evidence creation
* File validation
* URL validation
* Text extraction
* Chunking
* Embedding pipeline
* Retrieval
* Relationship schema validation
* AI response validation

### Frontend

Test:

* Evidence upload
* Canvas interactions
* Card movement
* Search
* Filters
* Evidence selection
* Relationship inspection
* Timeline navigation

---

# 39. Environment Variables

Use:

```env
OPENAI_API_KEY=
```

Never hardcode API keys.

Provide:

```text
.env.example
```

---

# 40. README

Create a professional README containing:

* Project overview
* Features
* Architecture
* Tech stack
* RAG pipeline
* AI relationship pipeline
* Installation
* Environment setup
* Running frontend
* Running backend
* API overview
* Project structure
* Demo workflow

---

# 41. MVP Boundaries

Do NOT over-engineer the project.

The MVP must prioritize:

### Essential

* Professional landing page
* Workspace
* Infinite canvas
* Evidence cards
* PDF upload
* Image upload
* URL ingestion
* Notes
* Evidence processing
* RAG retrieval
* AI Q&A
* Entity extraction
* Relationship detection
* Visual connections
* Source viewer
* Timeline
* Filters
* Persistence
* Demo workspace

### Optional if time permits

* PNG canvas export
* Advanced graph mode
* Multi-select operations
* Advanced relationship editing
* Additional file formats

Do not build:

* Multi-user collaboration
* Complex authentication
* Enterprise permissions
* Real-time multiplayer editing
* Payment system
* Kubernetes
* Microservices
* Complex cloud infrastructure

---

# 42. Definition of Done

The project is complete when:

* The application starts successfully.
* The landing page looks production-quality.
* A user can create an investigation workspace.
* A user can upload evidence.
* A user can add URLs.
* A user can create notes.
* Evidence is processed successfully.
* Evidence is chunked and embedded.
* RAG retrieval works.
* Users can ask questions about their evidence.
* AI answers contain source references.
* Entities are extracted.
* Relationships are generated.
* Relationships appear visually on the canvas.
* Evidence cards can be moved.
* Canvas supports zoom and pan.
* Timeline is generated from evidence.
* Filters work.
* Source viewer works.
* Workspace state persists after refresh.
* Demo data is available.
* Validation is implemented.
* Errors are handled gracefully.
* No API keys are exposed to the frontend.
* README explains setup and architecture.

---

# 43. Implementation Priority

Build in this order:

### Phase 1 — Foundation

* Project setup
* Frontend structure
* FastAPI setup
* API architecture
* Storage
* Environment configuration

### Phase 2 — Core UI

* Landing page
* Workspace layout
* Sidebar
* Canvas
* Evidence cards
* Navigation
* Modals
* Responsive layout

### Phase 3 — Evidence

* Upload
* URL ingestion
* Notes
* Evidence metadata
* Source viewer
* Validation

### Phase 4 — RAG

* Text extraction
* Chunking
* Embeddings
* Vector search
* Retrieval
* Grounded AI answers
* Source citations

### Phase 5 — Intelligence

* Entity extraction
* Topic extraction
* Event extraction
* Relationship detection
* Confidence scoring

### Phase 6 — Visual Intelligence

* Relationship lines
* Relationship inspector
* Timeline
* Graph view
* Filtering
* Highlighting
* Auto-layout

### Phase 7 — Polish

* Loading states
* Error states
* Animations
* Responsive behavior
* Demo data
* Export
* Testing
* README

---

# 44. Final Product Principle

The application should NOT feel like:

> "A chatbot that accepts documents."

It should feel like:

> **"A visual intelligence workspace where evidence becomes connected knowledge."**

The **canvas is the hero**.

RAG provides the intelligence underneath it.

The frontend must make the underlying AI infrastructure immediately understandable to a client or portfolio viewer without requiring them to understand the implementation.
