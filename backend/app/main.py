import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api import workspaces, evidence, search, relationships, export

# Data directories to ensure exist on startup
DATA_DIRS = [
    "data/workspaces",
    "data/evidence",
    "data/embeddings",
    "data/relationships",
    "data/timelines",
    "data/exports",
    "data/uploads",
]

BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
FRONTEND_DIR = BASE_DIR.parent / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create data directories on startup
    for dir_path in DATA_DIRS:
        (BASE_DIR / dir_path).mkdir(parents=True, exist_ok=True)
    print(f"[OK] Data directories ready")
    print(f"[OK] Frontend: {FRONTEND_DIR}")
    print(f"[OK] API docs: http://localhost:8000/docs")
    print(f"[OK] App:      http://localhost:8000")
    yield


app = FastAPI(
    title="AI Evidence Canvas",
    description="Visual AI investigation workspace — connect evidence, discover relationships, ask questions using RAG.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(workspaces.router, prefix="/api", tags=["Workspaces"])
app.include_router(evidence.router, prefix="/api", tags=["Evidence"])
app.include_router(search.router, prefix="/api", tags=["Search & AI"])
app.include_router(relationships.router, prefix="/api", tags=["Relationships"])
app.include_router(export.router, prefix="/api", tags=["Export"])


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


# Serve frontend static files (must be LAST)
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
else:
    @app.get("/")
    async def root():
        return {"message": "AI Evidence Canvas API", "docs": "/docs", "note": "Frontend not found. Place frontend/ next to backend/."}
