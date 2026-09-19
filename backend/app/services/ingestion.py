import logging
from pathlib import Path
from urllib.parse import urlparse
import httpx

from app.config import settings
from app.services.extraction import extract_from_pdf, extract_from_image, extract_from_url, extract_from_text
from app.services.ai import summarize_evidence, extract_entities_and_topics
from app.services.embeddings import embed_evidence
from app.services.relationship_engine import find_relationships_for_evidence
# Assume app.storage exists for DB operations
# from app.storage import db

logger = logging.getLogger(__name__)

async def process_evidence(evidence_id: str, workspace_id: str):
    """
    Full evidence processing pipeline.
    """
    try:
        logger.info(f"Processing evidence {evidence_id} in workspace {workspace_id}")
        # 1. Update status to PROCESSING
        # await db.update_evidence_status(evidence_id, "PROCESSING")
        
        # 2. Extract text based on evidence type
        # evidence = await db.get_evidence(evidence_id)
        # file_path = evidence.file_path
        # ev_type = evidence.type
        file_path = "mock_path.pdf" # Placeholder
        ev_type = "pdf"
        
        extracted_data = {}
        if ev_type == "pdf":
            extracted_data = await extract_from_pdf(file_path)
        elif ev_type in ["image", "png", "jpg", "jpeg"]:
            extracted_data = await extract_from_image(file_path)
        elif ev_type == "url":
            extracted_data = await extract_from_url(file_path)
        else:
            extracted_data = await extract_from_text("Mock content", "mock.txt")
            
        text = extracted_data.get("text", "")
        
        # 3. Update status to ANALYZING
        # await db.update_evidence_status(evidence_id, "ANALYZING")
        
        # 4. Generate summary
        summary = await summarize_evidence(text, ev_type)
        
        # 5. Extract entities, topics, events, claims, dates
        entities_data = await extract_entities_and_topics(text)
        
        # 6. Update status to FINDING_RELATIONSHIPS
        # await db.update_evidence_status(evidence_id, "FINDING_RELATIONSHIPS")
        
        # 7. Chunk text + generate embeddings + store in vector store
        metadata = {"source_type": ev_type, "source_name": Path(file_path).name}
        chunks = await embed_evidence(evidence_id, text, metadata)
        # await db.store_embeddings(chunks)
        
        # 8. Detect relationships with existing evidence in workspace
        # await db.save_evidence_metadata(evidence_id, summary, entities_data)
        new_relationships = await find_relationships_for_evidence(evidence_id, workspace_id)
        
        # 9. Update status to READY
        # await db.update_evidence_status(evidence_id, "READY")
        
        # 10. Update evidence quality checklist
        # quality = evaluate_quality(extracted_data)
        # await db.update_evidence_quality(evidence_id, quality)
        
    except Exception as e:
        logger.error(f"Pipeline failed for {evidence_id}: {e}")
        # await db.update_evidence_status(evidence_id, "FAILED", error_message=str(e))

async def process_url_evidence(evidence_id: str, url: str, workspace_id: str):
    """Specialized pipeline for URL evidence"""
    is_valid, msg = await validate_url(url)
    if not is_valid:
        # await db.update_evidence_status(evidence_id, "FAILED", error_message=msg)
        return
        
    await process_evidence(evidence_id, workspace_id)

async def validate_file(file_path: str, file_type: str) -> tuple[bool, str]:
    """Validate file exists, has valid extension, valid size"""
    path = Path(file_path)
    if not path.exists():
        return False, "File does not exist"
        
    allowed_exts = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".txt", ".md"}
    if path.suffix.lower() not in allowed_exts:
        return False, f"Invalid file extension. Allowed: {allowed_exts}"
        
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > settings.max_file_size_mb:
        return False, f"File too large. Max size: {settings.max_file_size_mb}MB"
        
    return True, ""

async def validate_url(url: str) -> tuple[bool, str]:
    """Validate URL is HTTP/HTTPS and reachable"""
    parsed = urlparse(url)
    if parsed.scheme not in ["http", "https"]:
        return False, "URL must use http or https scheme"
        
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.head(url, follow_redirects=True)
            if response.status_code >= 400:
                return False, f"URL returned status {response.status_code}"
    except Exception as e:
        return False, f"Could not reach URL: {str(e)}"
        
    return True, ""
