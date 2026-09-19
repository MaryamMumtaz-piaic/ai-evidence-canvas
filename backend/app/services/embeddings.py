import logging
import openai
from typing import List, Dict, Any

from app.config import settings

logger = logging.getLogger(__name__)

client = openai.AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

async def generate_embedding(text: str) -> list:
    """Generate embedding for a single text using text-embedding-3-small"""
    if not client: return []
    try:
        response = await client.embeddings.create(
            input=text,
            model=settings.embedding_model
        )
        return response.data[0].embedding
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return []

async def generate_embeddings_batch(texts: list) -> list:
    """Generate embeddings for multiple texts in batch"""
    if not client: return [[] for _ in texts]
    try:
        response = await client.embeddings.create(
            input=texts,
            model=settings.embedding_model
        )
        return [data.embedding for data in response.data]
    except Exception as e:
        logger.error(f"Error generating batch embeddings: {e}")
        return [[] for _ in texts]

def chunk_text(text: str, chunk_size: int = settings.max_chunk_size, overlap: int = settings.chunk_overlap) -> list:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        
        if end < text_length:
            last_period = text.rfind('.', start, end)
            last_newline = text.rfind('\n', start, end)
            break_point = max(last_newline, last_period)
            
            if break_point > start + (chunk_size // 2):
                end = break_point + 1
                
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
            
        start = end - overlap
        
    return chunks

async def embed_evidence(evidence_id: str, text: str, metadata: dict) -> list:
    """Chunk text, generate embeddings, return list of {chunk_id, embedding, metadata}"""
    chunks = chunk_text(text)
    embeddings = await generate_embeddings_batch(chunks)
    
    results = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        if not embedding:
            continue
            
        chunk_metadata = metadata.copy()
        chunk_metadata.update({
            "evidence_id": evidence_id,
            "chunk_index": i,
            "text": chunk
        })
        
        results.append({
            "chunk_id": f"{evidence_id}_chunk_{i}",
            "embedding": embedding,
            "metadata": chunk_metadata
        })
        
    return results
