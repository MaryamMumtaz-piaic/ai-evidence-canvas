import logging
from app.config import settings
from app.services.embeddings import generate_embedding
from app.services.ai import answer_question as ai_answer_question
# from app.storage import db

logger = logging.getLogger(__name__)

async def semantic_search(query: str, workspace_id: str, top_k: int = settings.rag_top_k) -> list:
    """
    1. Generate query embedding
    2. Search vector store for workspace
    3. Return top_k chunks with metadata
    """
    query_embedding = await generate_embedding(query)
    if not query_embedding:
        return []
        
    # chunks = await db.vector_search(workspace_id, query_embedding, top_k)
    chunks = []
    
    results = []
    for chunk in chunks:
        results.append({
            "chunk_text": chunk.get("text", ""),
            "evidence_id": chunk.get("evidence_id", ""),
            "source_name": chunk.get("source_name", ""),
            "similarity_score": chunk.get("score", 0.0),
            "page": chunk.get("page", None)
        })
    return results

async def ask_question(question: str, workspace_id: str) -> dict:
    """
    Full RAG pipeline.
    """
    chunks = await semantic_search(question, workspace_id)
    
    if not chunks:
        return {
            "answer": "No relevant context found in this workspace.",
            "sources": [],
            "confidence": 0.0
        }
        
    result = await ai_answer_question(question, chunks)
    return result

async def search_evidence_by_text(query: str, workspace_id: str) -> list:
    """
    Simple text search across evidence titles, content, entities, topics.
    Returns list of evidence IDs with match scores.
    """
    # results = await db.full_text_search(workspace_id, query)
    results = []
    return results
