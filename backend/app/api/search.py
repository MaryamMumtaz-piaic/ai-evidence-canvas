from fastapi import APIRouter
from app.schemas.ai import SearchQuery, SearchResponse, AskQuery, AskResponse

router = APIRouter(tags=["Search & AI"])

@router.post("/workspaces/{id}/search", response_model=SearchResponse)
async def semantic_search(id: str, query: SearchQuery):
    # Stub
    return {"results": []}

@router.post("/workspaces/{id}/ask", response_model=AskResponse)
async def ask_question(id: str, query: AskQuery):
    # Stub
    return {"answer": "Stub answer", "sources": [], "confidence": 0.0}
